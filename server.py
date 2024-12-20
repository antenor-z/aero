from os import environ
from fastapi import FastAPI, HTTPException, Request, Depends, Response
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from DB.Getter import get_all_icao, get_all_locations, get_all_names, get_info, latest_n_metars_parsed
from blueprints.admin import NotAllowedToEditAirport, NotLoggedException, NotSuperUser, admin, get_logged_user
from ext import IcaoError, get_metar, update_metars, update_tafs, get_taf
from historyPlot import update_df, update_images
from metarDecoder import DecodeError, decode_metar, get_wind_info
from tafDecoder import decode_taf
from util import windcross_filter, windhead_filter
from wind.Wind import get_components, get_components_one_runway, get_wind
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from starlette.middleware.sessions import SessionMiddleware
from translation import custom_errors
from version import VERSION
from contextlib import asynccontextmanager

scheduler = AsyncIOScheduler()
@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()
    yield
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory="templates")
templates.env.filters['frequency3'] = lambda value: "{:.3f}".format(round(float(value) / 1000, 3))
templates.env.filters['frequency1'] = lambda value: "{:.1f}".format(round(float(value) / 10, 1))
templates.env.filters['windhead'] = windhead_filter
templates.env.filters['windcross'] = windcross_filter

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(admin)

scheduler.add_job(update_metars, CronTrigger(minute='0,20,40', jitter=30))
scheduler.add_job(update_images, CronTrigger(minute='0,20,40'))
scheduler.add_job(update_df, CronTrigger(minute='0,20,40'))
scheduler.add_job(update_tafs, CronTrigger(hour='0,3,6,9,12,15,18,21', jitter=30))

with open(environ["SESSION_SECRET_KEY"]) as fp:
    SESSION_SECRET_KEY = fp.read()
app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET_KEY)



@app.get("/", response_class=HTMLResponse)
async def list_all(request: Request):
    try:
        user = get_logged_user(request=request,)
        airports = get_all_names(only_published=False)
        return templates.TemplateResponse("index.html", {"request": request,
                                                         "airports": airports,
                                                         "isLogged": True,
                                                         "isSuper": user.IsSuper,
                                                         "VERSION": VERSION})
    except:
        airports = get_all_names()
        return templates.TemplateResponse("index.html", {"request": request,
                                                         "airports": airports,
                                                         "isLogged": False,
                                                         "VERSION": VERSION})

@app.get("/info/{icao}", response_class=HTMLResponse)
async def info(request: Request, icao: str):
    icao_upper = icao.upper()
    if icao != icao_upper:
        return RedirectResponse(url=f"/info/{icao_upper}")
    
    try:
        get_logged_user(request=request,)
        return RedirectResponse(url=f"/area/restrita/info/{icao_upper}")
    except:
        pass

    try:
        info = await get_info(icao)
    except ValueError:
        raise HTTPException(status_code=404, detail="Aeroporto não encontrado")

    try:
        metar = await get_metar(icao)
        decoded = await decode_metar(metar)
    except Exception:
        decoded = [("", "Não foi possível obter o METAR")]

    go_back = "/mapa" if request.query_params.get("mapa") == "1" else "/"
    return templates.TemplateResponse("airport.html", 
                                      {"request": request, 
                                       "info": info, 
                                       "icao": icao, 
                                       "metar": metar,
                                       "go_back": go_back,
                                       "decoded": decoded})

@app.get("/taf/{icao}", response_class=HTMLResponse)
async def info_taf(request: Request, icao: str):
    icao_upper = icao.upper()
    if icao != icao_upper:
        return RedirectResponse(url=f"/info/taf/{icao_upper}")

    try:
        taf = await get_taf(icao)
    except Exception:
        raise HTTPException(status_code=400, detail="Aeroporto não encontrado")

    try:
        info = await get_info(icao)
        decoded = await decode_taf(taf)
    except Exception:
        raise HTTPException(status_code=400, detail="Erro ao obter o TAF")

    return templates.TemplateResponse("taf.html", {"request": request, "info": info, "icao": icao, "taf": taf, "decoded": decoded})

@app.get("/wind/", response_class=HTMLResponse)
async def wind(request: Request):
    return templates.TemplateResponse("wind.html", {"request": request})

@app.get("/windcalc/")
async def windcalc(request: Request):
    try:
        runway_head = int(request.query_params["runway_head"])
        wind_dir = int(request.query_params["wind_dir"])
        wind_speed = int(request.query_params["wind_speed"])
    except KeyError:
        raise HTTPException(status_code=400, detail="missing args")
    except ValueError:
        raise HTTPException(status_code=400, detail="invalid args")

    ret = get_components_one_runway(
        runway_head=runway_head,
        wind_dir=wind_dir,
        wind_speed=wind_speed)
    return ret

@app.get("/descent", response_class=HTMLResponse)
async def descent(request: Request):
    return templates.TemplateResponse("vertical.html", {"request": request})

@app.get("/history/{icao}/", response_class=HTMLResponse)
@app.get("/history/{icao}/{page}", response_class=HTMLResponse)
async def history(request: Request, icao: str, page: int=1):
    if not 1 <= page <= 5:
        raise HTTPException(status_code=400, detail="Página não encontrada")
    try:
        info = await get_info(icao)
    except Exception:
        raise HTTPException(status_code=404, detail="Aeroporto não encontrado")
    return templates.TemplateResponse("history.html", {"request": request, "icao": icao, "info": info, "page": page})

@app.get("/mapa", response_class=HTMLResponse)
async def descent(request: Request):
    try:
        get_logged_user(request=request,)
        locations = get_all_locations(only_published=False)
        return templates.TemplateResponse("map.html", {"request": request, 
                                                       "locations": locations})
    except:
        locations = get_all_locations()
        return templates.TemplateResponse("map.html", {"request": request, 
                                                       "locations": locations})
    
@app.get("/wind/{icao}/")
async def rwy_info(request: Request, icao: str):
    try:
        metar = await get_metar(icao)
        wind_runway = await get_components(icao=icao, metar=metar)
    except Exception:
        raise HTTPException(status_code=404, detail="Aeroporto não encontrado")
    
    return templates.TemplateResponse("wind-runway.html", {"request": request, 
                                                           "wind_runway": wind_runway})



@app.get("/favicon.ico", response_class=FileResponse)
async def favicon():
    return FileResponse("static/favicon.ico")

@app.exception_handler(404)
async def not_found(request: Request, exc: HTTPException):
    return templates.TemplateResponse("error.html", {"request": request, "error": f"Erro 404 | Página não encontrada"}, status_code=404)

@app.exception_handler(400)
async def bad_request(request: Request, exc: HTTPException):
    return templates.TemplateResponse("error.html", {"request": request, "error": f"Erro 400 | Requisição inválida"}, status_code=400)

@app.exception_handler(401)
async def unauthorized(request: Request, exc: HTTPException):
    return templates.TemplateResponse("error.html", {"request": request, "error": f"Erro 401 | Não autorizado"}, status_code=401)

@app.exception_handler(ValueError)
async def value_error(request: Request, exc: ValueError):
    if len(exc.args) == 2:
        return templates.TemplateResponse("error.html", {"request": request,
                                                         "error": f"Erro 422 | {exc.args[0]}",
                                                         "details": [exc.args[1]]}, status_code=422)
    else:
        return templates.TemplateResponse("error.html", {"request": request,
                                                         "error": f"Erro 422 | {exc}"})


@app.exception_handler(RequestValidationError)
async def unprocessable(request: Request, exc: RequestValidationError):
    details = []
    for error in exc.errors():
        error_type = error['type']
        loc = error['loc'][1]
        input_value = error['input']

        # print("!!!!", error_type)
        msg = custom_errors.get(error_type, error['msg'])

        if 'ctx' in error:
            msg = msg.format(**error['ctx'])

        details.append(f"Variável '{loc}' com valor '{input_value}' está com o erro '{msg}'")

    return templates.TemplateResponse("error.html", {
        "request": request, 
        "error": "Erro 422 | Erro no formulário", 
        "details": details
    }, status_code=422)

@app.get("/download/excel/{icao}")
async def dump_metar_dataset(request: Request, icao: str):
    return FileResponse(
        f"static/datasets/dataset_{icao}.xlsx",
        media_type='application/octet-stream', 
        filename=f"dataset_{icao}.xlsx"
    )

@app.exception_handler(NotLoggedException)
async def not_logged_exception_handler(request: Request, exc: NotLoggedException):
    return RedirectResponse("/area/restrita/login", status_code=303)


@app.exception_handler(NotAllowedToEditAirport)
async def not_allowed_to_edit_airport_handler(request: Request, exc: NotAllowedToEditAirport):
    return templates.TemplateResponse("error.html", {"request": request, "error": "User can't edit this airport"})


@app.exception_handler(NotSuperUser)
async def not_super_user_handler(request: Request, exc: NotSuperUser):
    return templates.TemplateResponse("error.html", {"request": request, "error": "User can't create or remove airports"})

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="debug")

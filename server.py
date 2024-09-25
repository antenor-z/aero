from os import environ
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from DB.Getter import get_all_icao, get_all_names, get_info, latest_n_metars_parsed
from blueprints.admin import NotAllowedToEditAirport, NotLoggedException, NotSuperUser, admin, get_logged_user
from ext import IcaoError, get_metar, update_metars, update_tafs, get_taf
from historyPlot import update_images
from metarDecoder import DecodeError, decode_metar, get_wind_info
from tafDecoder import decode_taf
from wind.Wind import get_components, get_components_one_runway, get_wind
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from starlette.middleware.sessions import SessionMiddleware
from version import VERSION

app = FastAPI()
templates = Jinja2Templates(directory="templates")
templates.env.filters['frequency3'] = lambda value: "{:.3f}".format(round(float(value) / 1000, 3))
templates.env.filters['frequency1'] = lambda value: "{:.1f}".format(round(float(value) / 10, 1))
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(admin)

scheduler = BackgroundScheduler()
scheduler.add_job(update_metars, CronTrigger(minute='0,15,30,45'), args=[get_all_icao()])
scheduler.add_job(update_images, CronTrigger(minute='0,15,30,45'))
scheduler.add_job(update_tafs, CronTrigger(hour='10'), args=[get_all_icao()])
scheduler.start()

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
        info = get_info(icao)
    except Exception:
        raise HTTPException(status_code=404, detail="Aeroporto não encontrado")

    try:
        metar = get_metar(icao)
        decoded = decode_metar(metar)
    except Exception:
        decoded = [("", "Não foi possível obter o METAR")]

    return templates.TemplateResponse("airport.html", 
                                      {"request": request, 
                                       "info": info, 
                                       "icao": icao, 
                                       "metar": metar, 
                                       "decoded": decoded})

@app.get("/taf/{icao}", response_class=HTMLResponse)
async def info_taf(request: Request, icao: str):
    icao_upper = icao.upper()
    if icao != icao_upper:
        return RedirectResponse(url=f"/info/taf/{icao_upper}")

    try:
        taf = get_taf(icao)
    except Exception:
        raise HTTPException(status_code=400, detail="Aeroporto não encontrado")

    try:
        info = get_info(icao)
        decoded = decode_taf(taf)
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
async def history(request: Request, icao: str):
    try:
        info = get_info(icao)
    except Exception:
        raise HTTPException(status_code=404, detail="Aeroporto não encontrado")
    return templates.TemplateResponse("history.html", {"request": request, "icao": icao, "info": info})

@app.get("/favicon.ico", response_class=FileResponse)
async def favicon():
    return FileResponse("static/favicon.ico")

@app.exception_handler(404)
async def not_found(request: Request, exc: HTTPException):
    return templates.TemplateResponse("error.html", {"request": request, "error": f"Erro 404 | {exc.detail}"}, status_code=404)

@app.exception_handler(400)
async def bad_request(request: Request, exc: HTTPException):
    return templates.TemplateResponse("error.html", {"request": request, "error": f"Erro 400 | {exc.detail}"}, status_code=400)

@app.exception_handler(401)
async def unauthorized(request: Request, exc: HTTPException):
    return templates.TemplateResponse("error.html", {"request": request, "error": f"Erro 401 | {exc.detail}"}, status_code=401)

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
async def unprocesable(request: Request, exc: RequestValidationError):
    details = []
    for error in exc.errors():
        details.append(f"Variável '{error["loc"][1]}' com valor '{error["input"]}' está com o erro '{error["msg"]}'")
    return templates.TemplateResponse("error.html", {"request": request, 
                                                     "error": f"Erro 422 | Erro no formulário", 
                                                     "details": details},
                                                     status_code=401)


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

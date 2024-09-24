from fastapi import APIRouter, Form, HTTPException, Request, status
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import Optional

from DB.AdminGetter import get_aerodrome, get_cities, get_comm_types, get_communication, get_ils, get_ils_categories, \
    get_pavement_codes, get_runway, get_user, get_vor, get_states, get_city
from DB.AdminSetter import create_city, create_comm, create_ils, create_runway, create_vor, del_aerodrome, \
    del_comm, del_ils, del_runway, del_vor, patch_aerodrome, patch_ils, patch_runway, patch_comm, patch_vor, \
    create_aerodrome, publish_aerodrome, unpublish_aerodrome
from DB.Getter import get_all_names, get_info
from DB.ORM import User
from ext import get_metar
from metarDecoder import decode_metar
from security import password
from util import get_city_and_code_from_IGBE

admin = APIRouter()

templates = Jinja2Templates(directory="templates")
templates.env.filters['frequency3'] = lambda value: "{:.3f}".format(round(float(value) / 1000, 3))
templates.env.filters['frequency1'] = lambda value: "{:.1f}".format(round(float(value) / 10, 1))
admin.mount("/static", StaticFiles(directory="static"), name="static")


class NotLoggedException(Exception):
    ...


class NotAllowedToEditAirport(Exception):
    ...


class NotSuperUser(Exception):
    ...


def get_logged_user(request: Request, icao_to_check: Optional[str] = None, super_only: bool = False):
    username = request.session.get("logged_user")
    if username is None:
        raise NotLoggedException

    user: User = get_user(username=username)
    if user is None:
        raise NotLoggedException

    if not user.IsSuper and icao_to_check is not None:
        authorized_airports = user.CanEditAirportsList.split(",")
        if icao_to_check not in authorized_airports:
            raise NotAllowedToEditAirport

    if super_only and not user.IsSuper:
        raise NotSuperUser

    return user


@admin.get("/area/restrita", response_class=HTMLResponse)
async def restricted_area(request: Request):
    user: User = get_logged_user(request)
    return RedirectResponse("/")


@admin.get("/area/restrita/info/{icao}", response_class=HTMLResponse)
async def restricted_area_airport(request: Request, icao: str):
    get_logged_user(request, icao_to_check=icao)
    icao_upper = icao.upper()
    if icao != icao_upper:
        return RedirectResponse(f"/info/{icao_upper}")

    info = get_info(icao, only_published=False)

    try:
        metar = get_metar(icao)
        decoded = decode_metar(metar)
    except Exception:
        decoded = [("", "Não foi possível obter o METAR")]

    return templates.TemplateResponse("airport.html", {
        "request": request,
        "info": info,
        "icao": icao,
        "metar": metar,
        "decoded": decoded,
        "isLogged": True,
        "IsPublished": info["IsPublished"],
    })


@admin.get("/area/restrita/login", response_class=HTMLResponse)
async def get_login(request: Request):
    return templates.TemplateResponse("admin/login.html", {"request": request})


@admin.post("/area/restrita/login", response_class=HTMLResponse)
async def post_login(request: Request, user: str = Form(...), passwd: str = Form(...), totp: Optional[str] = Form(None)):
    try:
        user: User = password.authenticate(user_name=user, passwd=passwd, totp_token=totp)
        request.session["logged_user"] = user.Name
        return RedirectResponse("/area/restrita", status_code=303)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")


@admin.post("/area/restrita/logout", response_class=HTMLResponse)
async def logout(request: Request):
    get_logged_user(request=request)
    request.session.pop("logged_user")
    return RedirectResponse("/area/restrita", status_code=303)


@admin.get("/area/restrita/add", response_class=HTMLResponse)
async def add_aerodrome(request: Request):
    get_logged_user(request, super_only=True)
    empty_aerodrome = {
        "AerodromeName": "",
        "CityCode": "",
        "Latitude": "",
        "Longitude": ""
    }

    states = get_states()
    return templates.TemplateResponse("admin/airport.html", {
        "request": request,
        "icao": "",
        "action": "/area/restrita/add",
        "aerodrome": empty_aerodrome,
        "States": states,
        "StateCode": ""
    })


@admin.post("/area/restrita/add")
async def add_aerodrome_post(request: Request,
                             icao: str = Form(...),
                             aerodrome_name: str = Form(...),
                             latitude: float = Form(...),
                             longitude: float = Form(...),
                             city_name: str = Form(...),
                             state_code: str = Form(...)):

    get_logged_user(request, super_only=True)

    city = get_city(state_code=state_code, city_name=city_name.replace("+", " "))
    if not city:
        res = get_city_and_code_from_IGBE(city=city_name, state_code=int(state_code))
        if res is None:
            raise ValueError("Cidade inválida")
        city_code, city_name = res
        city = create_city(city_code=city_code, city_name=city_name, state_code=state_code)

    create_aerodrome(icao=icao,
                    aerodrome_name=aerodrome_name,
                    latitude=latitude,
                    longitude=longitude,
                    city_code=city.CityCode,
                    user=get_logged_user(request))

    return RedirectResponse(f"/area/restrita/info/{icao}", status_code=status.HTTP_303_SEE_OTHER)

@admin.get("/area/restrita/{icao}/edit")
async def edit_aerodrome(icao: str, request: Request):
    user = get_logged_user(request=request, icao_to_check=icao)
    aerodrome = get_aerodrome(icao=icao)
    return templates.TemplateResponse("admin/airport.html", {
        "request": request,
        "icao": icao,
        "action": f"/area/restrita/{icao}/edit",
        "aerodrome": aerodrome,
        "States": get_states(),
        "canDelete": user.IsSuper
    })

@admin.post("/area/restrita/{icao}/edit")
async def edit_aerodrome_post(request: Request,
                              icao: str,
                              aerodrome_name: str = Form(...),
                              latitude: float = Form(...),
                              longitude: float = Form(...),
                              city_name: str = Form(...),
                              state_code: str = Form(...)):
    user = get_logged_user(request=request, icao_to_check=icao, super_only=True)

    city = get_city(state_code=state_code, city_name=city_name)
    if city is None:
        res = get_city_and_code_from_IGBE(city=city_name, state_code=state_code)
        if res is None:
            raise ValueError("Cidade inválida")
        city_code, city_name = res
        city = create_city(city_code=city_code, city_name=city_name, state_code=state_code)

    patch_aerodrome(icao=icao,
                    aerodrome_name=aerodrome_name,
                    latitude=float(latitude),
                    longitude=float(longitude),
                    city_code=city.CityCode)
    return RedirectResponse(url=f"/area/restrita/info/{icao}", status_code=status.HTTP_303_SEE_OTHER)


@admin.post("/area/restrita/{icao}/delete")
async def delete_aerodrome(request: Request, icao: str):

    get_logged_user(request=request, icao_to_check=icao, super_only=True)

    del_aerodrome(icao)
    return RedirectResponse(url="/area/restrita", status_code=status.HTTP_303_SEE_OTHER)


@admin.get("/area/restrita/{icao}/runway/add")
async def add_runway(request: Request, icao: str):

    get_logged_user(request=request, icao_to_check=icao)

    empty_runway = {"Head1": "", "Head2": "", "RunwayLength": "", "RunwayWidth": "", "PavementCode": ""}
    return templates.TemplateResponse("admin/runway.html", {
        "request": request,
        "icao": icao,
        "runway": empty_runway,
        "action": f"/area/restrita/{icao}/runway/add",
        "pavementCodes": get_pavement_codes()
    })

@admin.post("/area/restrita/{icao}/runway/add")
async def add_runway(request: Request,
                     icao: str,
                     head1: str = Form(pattern="\d{2}[LRC]?"),
                     head2: str = Form(pattern="\d{2}[LRC]?"),
                     runway_length: int = Form(...),
                     runway_width: int = Form(...),
                     pavement_code: str = Form(...)):

    get_logged_user(request=request, icao_to_check=icao)

    create_runway(
        icao=icao, 
        head1=head1, 
        head2=head2, 
        runway_length=runway_length, 
        runway_width=runway_width, 
        pavement_code=pavement_code)
       
    return RedirectResponse(url=f"/area/restrita/info/{icao}", status_code=status.HTTP_303_SEE_OTHER)


@admin.get("/area/restrita/{icao}/runway/{runwayHead}/edit")
async def edit_runway(request: Request, icao: str, runwayHead: str):

    get_logged_user(request=request, icao_to_check=icao)

    runway = get_runway(icao=icao, runway_head=runwayHead)
    return templates.TemplateResponse("admin/runway.html", {
        "request": request,
        "icao": icao,
        "runway": runway,
        "action": f"/area/restrita/{icao}/runway/{runwayHead}/edit",
        "pavementCodes": get_pavement_codes(),
        "canDelete": True
    })

@admin.post("/area/restrita/{icao}/runway/{runway_head}/edit")
async def edit_runway_post(request: Request,
                           icao: str,
                           runway_head: str,
                           head1: str = Form(pattern="\d{2}[LRC]?"),
                           head2: str = Form(pattern="\d{2}[LRC]?"),
                           runway_length: int = Form(...),
                           runway_width: int = Form(...),
                           pavement_code: str = Form(...)):
    
    get_logged_user(request=request, icao_to_check=icao)

    patch_runway(
        icao=icao, 
        head1_old=runway_head, 
        head1=head1, 
        head2=head2, 
        runway_length=runway_length, 
        runway_width=runway_width, 
        pavement_code=pavement_code)

    return RedirectResponse(url=f"/area/restrita/info/{icao}", status_code=status.HTTP_303_SEE_OTHER)


@admin.post("/area/restrita/{icao}/runway/{runwayHead}/delete")
async def delete_runway(request: Request, icao: str, runwayHead: str):

    get_logged_user(request=request, icao_to_check=icao)

    del_runway(icao, runwayHead)
    return RedirectResponse(url=f"/area/restrita/info/{icao}", status_code=status.HTTP_303_SEE_OTHER)


@admin.get("/area/restrita/{icao}/communication/add")
async def add_communication(request: Request, icao: str):

    get_logged_user(request=request, icao_to_check=icao)

    empty_comm = {"Frequency": "", "CommType": ""}
    return templates.TemplateResponse("admin/communication.html", {
        "request": request,
        "icao": icao,
        "communication": empty_comm,
        "action": f"/area/restrita/{icao}/communication/add",
        "commTypes": get_comm_types()
    })

@admin.post("/area/restrita/{icao}/communication/add")
async def add_communication_post(request: Request,
                                 icao: str,
                                 frequency: int = Form(...),
                                 comm_type: str = Form(...)):
    
    get_logged_user(request=request, icao_to_check=icao)

    create_comm(icao=icao, frequency=frequency, comm_type=comm_type)

    return RedirectResponse(url=f"/area/restrita/info/{icao}", status_code=status.HTTP_303_SEE_OTHER)


@admin.get("/area/restrita/{icao}/communication/{frequency}/edit")
async def edit_communication(request: Request,
                             icao: str,
                             frequency: int):
    
    get_logged_user(request=request, icao_to_check=icao)

    comm = get_communication(icao=icao, frequency=frequency)
    return templates.TemplateResponse("admin/communication.html", {
        "request": request,
        "icao": icao,
        "communication": comm,
        "action": f"/area/restrita/{icao}/communication/{frequency}/edit",
        "commTypes": get_comm_types(),
        "canDelete": True
    })

@admin.post("/area/restrita/{icao}/communication/{frequency_old}/edit")
async def edit_communication(request: Request,
                             icao: str,
                             frequency_old: int,
                             frequency: int = Form(...),
                             comm_type: str = Form(...)):
    
    get_logged_user(request=request, icao_to_check=icao)

    patch_comm(icao=icao, 
               frequency_old=frequency_old, 
               frequency=frequency, 
               comm_type=comm_type)

    return RedirectResponse(url=f"/area/restrita/info/{icao}", status_code=status.HTTP_303_SEE_OTHER)


@admin.post("/area/restrita/{icao}/communication/{frequency}/delete")
async def delete_communication(request: Request, icao: str, frequency: int):
    get_logged_user(request=request, icao_to_check=icao)
    del_comm(icao, frequency)
    return RedirectResponse(url=f"/area/restrita/info/{icao}", status_code=status.HTTP_303_SEE_OTHER)


@admin.get("/area/restrita/{icao}/ils/add")
async def add_ils(request: Request, icao: str):
    get_logged_user(request=request, icao_to_check=icao)
    if request.method == 'GET':
        empty_ils = {"Ident": "", "RunwayHead": "", "Frequency": "", "Category": "", "Crs": "", "Minimum": ""}
        return templates.TemplateResponse("admin/ils.html", {
            "request": request,
            "icao": icao,
            "ils": empty_ils,
            "action": f"/area/restrita/{icao}/ils/add",
            "ILS_Categories": get_ils_categories()
        })

@admin.post("/area/restrita/{icao}/ils/add")
async def add_ils_post(request: Request,
                       icao: str,
                       ident: str = Form(pattern="[A-Z]{3}"),
                       runway_head: str = Form(pattern="\d{2}[LRC]?"),
                       frequency: int = Form(...),
                       category: str = Form(...),
                       crs: int = Form(...),
                       minimum: int = Form(...)):
    get_logged_user(request=request, icao_to_check=icao)

    create_ils(
        icao=icao, 
        ident=ident, 
        runway_head=runway_head, 
        frequency=frequency, 
        category=category, 
        crs=crs, 
        minimum=minimum)

    return RedirectResponse(url=f"/area/restrita/info/{icao}", status_code=status.HTTP_303_SEE_OTHER)


@admin.get("/area/restrita/{icao}/ils/{frequency}/edit")
async def edit_ils(request: Request,
                   icao: str,
                   frequency: int):

    get_logged_user(request=request, icao_to_check=icao)

    ils = get_ils(icao=icao, frequency=frequency)
    return templates.TemplateResponse("admin/ils.html", {
        "request": request,
        "icao": icao,
        "ils": ils,
        "action": f"/area/restrita/{icao}/ils/{frequency}/edit",
        "ILS_Categories": get_ils_categories(),
        "canDelete": True
    })

@admin.post("/area/restrita/{icao}/ils/{frequency_old}/edit")
async def edit_ils(request: Request,
                   icao: str,
                   frequency_old: int,
                   ident: str = Form(pattern="[A-Z]{3}"),
                   runway_head: str = Form(pattern="\d{2}[LRC]?"),
                   frequency: int = Form(...),
                   category: str = Form(...),
                   crs: int = Form(...),
                   minimum: int = Form(...)):
    
    get_logged_user(request=request, icao_to_check=icao)

    patch_ils(icao=icao, 
              frequency_old=frequency_old, 
              ident=ident, 
              runway_head=runway_head, 
              frequency=frequency, 
              category=category, 
              crs=crs, 
              minimum=minimum)

    return RedirectResponse(url=f"/area/restrita/info/{icao}", status_code=status.HTTP_303_SEE_OTHER)


@admin.post("/area/restrita/{icao}/ils/{frequency}/delete")
async def delete_ils(request: Request,
                     icao: str,
                     frequency: int):

    get_logged_user(request=request, icao_to_check=icao)
    del_ils(icao, frequency)
    return RedirectResponse(url=f"/area/restrita/info/{icao}", status_code=status.HTTP_303_SEE_OTHER)


@admin.get("/area/restrita/{icao}/vor/add")
async def add_vor(request: Request,
                  icao: str):

    get_logged_user(request=request, icao_to_check=icao)
    if request.method == 'GET':
        empty_vor = {"Ident": "", "Frequency": ""}
        return templates.TemplateResponse("admin/vor.html", {
            "request": request,
            "icao": icao,
            "vor": empty_vor,
            "action": f"/area/restrita/{icao}/vor/add",
        })
    
@admin.post("/area/restrita/{icao}/vor/add")
async def add_vor(request: Request,
                  icao: str,
                  ident: str = Form(pattern="[A-Z]{3}"),
                  frequency: int = Form(...)): 

    get_logged_user(request=request, icao_to_check=icao)

    create_vor(
        icao=icao, 
        ident=ident, 
        frequency=frequency)

    return RedirectResponse(url=f"/area/restrita/info/{icao}", status_code=status.HTTP_303_SEE_OTHER)


@admin.get("/area/restrita/{icao}/vor/{frequency}/edit")
async def edit_vor(request: Request,
                   icao: str,
                   frequency: int):
    get_logged_user(request=request, icao_to_check=icao)
   
    vor = get_vor(icao=icao, frequency=frequency)
    return templates.TemplateResponse("admin/vor.html", {
        "request": request,
        "icao": icao,
        "vor": vor,
        "action": f"/area/restrita/{icao}/vor/{frequency}/edit",
        "canDelete": True
    })

@admin.post("/area/restrita/{icao}/vor/{frequency_old}/edit")
async def edit_vor_post(request: Request,
                        icao: str,
                        frequency_old: int,
                        ident: str = Form(pattern="[A-Z]{3}"),
                        frequency: int = Form(...)):
    get_logged_user(request=request, icao_to_check=icao)


    patch_vor(
        icao=icao, 
        frequency_old=frequency_old, 
        ident=ident, 
        frequency=frequency)

    return RedirectResponse(url=f"/area/restrita/info/{icao}", status_code=status.HTTP_303_SEE_OTHER)


@admin.post("/area/restrita/{icao}/vor/{frequency}/delete")
async def delete_vor(request: Request,
                     icao: str,
                     frequency: int):
    get_logged_user(request=request, icao_to_check=icao)
    del_vor(icao, frequency)
    return RedirectResponse(url=f"/area/restrita/info/{icao}", status_code=status.HTTP_303_SEE_OTHER)

@admin.get("/area/restrita/{icao}/publish", response_class=HTMLResponse)
async def publish_aerodrome_post(request: Request,
                            icao: str,
                            ):
    get_logged_user(request=request, icao_to_check=icao)
    publish_aerodrome(icao=icao)
    return RedirectResponse(url=f"/area/restrita/info/{icao}")


@admin.get("/area/restrita/{icao}/unpublish", response_class=HTMLResponse)
async def publish_aerodrome_post(request: Request,
                            icao: str,
                            ):
    get_logged_user(request=request, icao_to_check=icao)
    unpublish_aerodrome(icao=icao)
    return RedirectResponse(url=f"/area/restrita/info/{icao}")

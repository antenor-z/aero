from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from typing import Optional

from DB.AdminGetter import get_aerodrome, get_cities, get_comm_types, get_communication, get_ils, get_ils_categories, \
    get_pavement_codes, get_runway, get_user, get_vor, get_states, get_city
from DB.AdminSetter import create_city, create_comm, create_ils, create_runway, create_vor, del_aerodrome, \
    del_comm, del_ils, del_runway, del_vor, patch_aerodrome, patch_ils, patch_runway, patch_comm, patch_vor, \
    create_aerodrome
from DB.Getter import get_all_names, get_info
from DB.ORM import User
from ext import get_metar
from metarDecoder import decode_metar
from security import password
from util import get_city_and_code_from_IGBE

admin = APIRouter()
admin.add_middleware(SessionMiddleware, secret_key="your_secret_key")

templates = Jinja2Templates(directory="templates")
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

    if icao_to_check is not None and not user.IsSuper:
        authorized_airports = user.CanEditAirportsList.split(",")
        if icao_to_check not in authorized_airports:
            raise NotAllowedToEditAirport

    if super_only and not user.IsSuper:
        raise NotSuperUser

    return user


@admin.get("/area/restrita", response_class=HTMLResponse)
async def restricted_area(request: Request):
    user: User = get_logged_user(request)

    allowed_aerodromes_list = []
    for aerodrome_name, ICAO, _ in get_all_names():
        if ICAO in user.CanEditAirportsList.split(","):
            allowed_aerodromes_list.append((ICAO, aerodrome_name))

    return templates.TemplateResponse("admin/index.html", {
        "request": request,
        "allowed_aerodromes_list": allowed_aerodromes_list,
        "canCreate": user.IsSuper
    })


@admin.get("/area/restrita/{icao}", response_class=HTMLResponse)
async def restricted_area_airport(request: Request, icao: str):
    get_logged_user(request, icao_to_check=icao)
    icao_upper = icao.upper()
    if icao != icao_upper:
        return RedirectResponse(f"/info/{icao_upper}")

    try:
        info = get_info(icao)
    except Exception:
        return templates.TemplateResponse("error.html", {"request": request, "error": "Aeroporto não encontrado"}, status_code=400)

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
        "isLogged": True
    })


@admin.get("/area/restrita/login", response_class=HTMLResponse)
async def get_login(request: Request):
    return templates.TemplateResponse("admin/login.html", {"request": request})


@admin.post("/area/restrita/login", response_class=HTMLResponse)
async def post_login(request: Request, user: str = Form(...), password: str = Form(...), totp: str = Form(...)):
    try:
        user: User = password.authenticate(user_name=user, passwd=password, totp_token=totp)
        request.session["logged_user"] = user.Name
        return RedirectResponse("/area/restrita", status_code=303)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid credentials")


@admin.get("/area/restrita/logout", response_class=HTMLResponse)
async def get_logout(request: Request):
    request.session.pop("logged_user")
    return RedirectResponse("/area/restrita", status_code=303)


@admin.get("/area/restrita/add", response_class=HTMLResponse)
async def add_aerodrome_get(request: Request):
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
async def add_aerodrome_post(request: Request, icao: str = Form(...), aerodrome_name: str = Form(...),
                             latitude: float = Form(...), longitude: float = Form(...),
                             city_name: str = Form(...), state_code: str = Form(...)):
    get_logged_user(request, super_only=True)

    city = get_city(state_code=state_code, city_name=city_name.replace("+", " "))
    if not city:
        res = get_city_and_code_from_IGBE(city=city_name, state_code=state_code)
        if res is None:
            return HTMLResponse("Cidade inválida", status_code=400)
        city_code, city_name = res
        city = create_city(city_code=city_code, city_name=city_name, state_code=state_code)

    create_aerodrome(icao=icao,
                     aerodrome_name=aerodrome_name,
                     latitude=latitude,
                     longitude=longitude,
                     city_code=city.CityCode,
                     user=get_logged_user(request))

    return RedirectResponse(f"/area/restrita/{icao}", status_code=303)

# @admin.route("/area/restrita/<string:icao>/edit", methods=['GET', 'POST'])
# def edit_aerodrome(icao: str):
#     if request.method == 'GET':
#         user = get_logged_user(icao_to_check=icao)
#         aerodrome = get_aerodrome(icao=icao)
#         return render_template("admin/airport.html",
#                                icao=icao,
#                                action=f"/area/restrita/{icao}/edit",
#                                aerodrome=aerodrome,
#                                States=get_states(),
#                                canDelete=user.IsSuper)
#     else:
#         user = get_logged_user(icao_to_check=icao, super_only=True)
#         icao = request.form.get('ICAO')
#         aerodrome_name = request.form.get('AerodromeName')
#         latitude = request.form.get('Latitude')
#         longitude = request.form.get('Longitude')
#         city_name = request.form.get('CityName').replace("+", " ")
#         state_code = request.form.get('StateCode')

#         city = get_city(state_code=state_code, city_name=city_name)

#     if city is None:
#         res = get_city_and_code_from_IGBE(city=city_name, state_code=state_code)
#         if res is None:
#             return "Cidade inválida"
#         city_code, city_name = res
#         city = create_city(city_code=city_code, city_name=city_name, state_code=state_code)

#     patch_aerodrome(icao=icao,
#                     aerodrome_name=aerodrome_name,
#                     latitude=float(latitude),
#                     longitude=float(longitude),
#                     city_code=city.CityCode)
#     return redirect(f"/area/restrita/{icao}")


# @admin.post("/area/restrita/<string:icao>/delete")
# def delete_aerodrome(icao: str):
#     get_logged_user(icao_to_check=icao, super_only=True)
#     del_aerodrome(icao)
#     return redirect("/area/restrita")


# @admin.route("/area/restrita/<string:icao>/runway/add", methods=['GET', 'POST'])
# def add_runway(icao: str):
#     get_logged_user(icao_to_check=icao)
#     if request.method == 'GET':
#         empty_runway = {"Head1": "", "Head2": "", "RunwayLength": "", "RunwayWidth": "", "PavementCode": ""}
#         print(get_pavement_codes())
#         return render_template("admin/runway.html",
#                                icao=icao,
#                                runway=empty_runway,
#                                action=f"/area/restrita/{icao}/runway/add",
#                                pavementCodes=get_pavement_codes())
#     else:
#         head1 = request.form.get('Head1')
#         head2 = request.form.get('Head2')
#         runway_length = request.form.get('RunwayLength')
#         runway_width = request.form.get('RunwayWidth')
#         pavement_code = request.form.get('PavementCode')

#         if (exc := create_runway(icao=icao, 
#                                  head1=head1, 
#                                  head2=head2, 
#                                  runway_length=runway_length, 
#                                  runway_width=runway_width, 
#                                  pavement_code=pavement_code)) is not None:
#             return exc, 401

#         return redirect(f"/area/restrita/{icao}")


# @admin.route("/area/restrita/<string:icao>/runway/<string:runwayHead>/edit", methods=['GET', 'POST'])
# def edit_runway(icao: str, runwayHead):
#     get_logged_user(icao_to_check=icao)
#     if request.method == 'GET':
#         runway = get_runway(icao=icao, runway_head=runwayHead)
#         return render_template("admin/runway.html",
#                                icao=icao,
#                                runway=runway,
#                                action=f"/area/restrita/{icao}/runway/{runwayHead}/edit",
#                                pavementCodes=get_pavement_codes(),
#                                canDelete=True
#                                )
#     else:
#         head1 = request.form.get('Head1')
#         head2 = request.form.get('Head2')
#         runway_length = request.form.get('RunwayLength')
#         runway_width = request.form.get('RunwayWidth')
#         pavement_code = request.form.get('PavementCode')

#         if (exc := patch_runway(icao=icao, 
#                                 head1_old=runwayHead, 
#                                 head1=head1, 
#                                 head2=head2, 
#                                 runway_length=runway_length, 
#                                 runway_width=runway_width, 
#                                 pavement_code=pavement_code)) is not None:
#             return exc, 401
   
#         return redirect(f"/area/restrita/{icao}")


# @admin.post("/area/restrita/<string:icao>/runway/<string:runwayHead>/delete")
# def delete_runway(icao: str, runwayHead: str):
#     get_logged_user(icao_to_check=icao)
#     del_runway(icao, runwayHead)
#     return redirect(f"/area/restrita/{icao}")


# @admin.route("/area/restrita/<string:icao>/communication/add", methods=['GET', 'POST'])
# def add_communication(icao: str):
#     get_logged_user(icao_to_check=icao)
#     if request.method == 'GET':
#         empty_comm = {"Frequency": "", "CommType": ""}
#         return render_template("admin/communication.html",
#                                icao=icao,
#                                communication=empty_comm,
#                                action=f"/area/restrita/{icao}/communication/add",
#                                CommTypes=get_comm_types())
#     else:
#         frequency = request.form.get('Frequency')
#         comm_type = request.form.get('CommType')

#         if (exc := create_comm(icao=icao, frequency=frequency, comm_type=comm_type)) is not None:
#             return exc, 401

#         return redirect(f"/area/restrita/{icao}")


# @admin.route("/area/restrita/<string:icao>/communication/<int:frequency>/edit", methods=['GET', 'POST'])
# def edit_communication(icao: str, frequency: int):
#     get_logged_user(icao_to_check=icao)
#     if request.method == 'GET':
#         communication = get_communication(icao=icao, frequency=frequency)
#         return render_template("admin/communication.html",
#                                icao=icao,
#                                communication=communication,
#                                action=f"/area/restrita/{icao}/communication/{frequency}/edit",
#                                CommTypes=get_comm_types(),
#                                canDelete=True)
#     else:
#         frequency_new = request.form.get('Frequency')
#         comm_type = request.form.get('CommType')

#         if (exc := patch_comm(icao, frequency, frequency_new, comm_type)) is not None:
#             return exc, 401

#         return redirect(f"/area/restrita/{icao}")


# @admin.post("/area/restrita/<string:icao>/communication/<int:frequency>/delete")
# def delete_communication(icao: str, frequency: int):
#     get_logged_user(icao_to_check=icao)
#     del_comm(icao, frequency)
#     return redirect(f"/area/restrita/{icao}")


# @admin.route("/area/restrita/<string:icao>/ils/add", methods=['GET', 'POST'])
# def add_ils(icao: str):
#     get_logged_user(icao_to_check=icao)
#     if request.method == 'GET':
#         ils = {"Ident": "", 
#                "RunwayHead": "",
#                "Frequency": "",
#                "Category": "",
#                "CRS": "",
#                "Minimum": ""}
#         return render_template("admin/ils.html",
#                                icao=icao,
#                                ils=ils,
#                                action=f"/area/restrita/{icao}/ils/add",
#                                ILSCats=get_ils_categories())
#     else:
#         ident = request.form.get('Ident')
#         runway_head = request.form.get('RunwayHead')
#         frequency = request.form.get('Frequency')
#         category = request.form.get('Category')
#         crs = request.form.get('CRS')
#         minimum = request.form.get('Minimum')

#         if (exc := create_ils(icao=icao,
#                               ident=ident, 
#                               runway_head=runway_head, 
#                               frequency=frequency, 
#                               category=category, 
#                               crs=crs, 
#                               minimum=minimum)) is not None:
#             return exc, 401

#         return redirect(f"/area/restrita/{icao}")


# @admin.route("/area/restrita/<string:icao>/ils/<int:frequency>/edit", methods=['GET', 'POST'])
# def edit_ils(icao: str, frequency: int):
#     get_logged_user(icao_to_check=icao)
#     if request.method == 'GET':
#         ils = get_ils(icao=icao, frequency=frequency)
#         return render_template("admin/ils.html",
#                                icao=icao,
#                                ils=ils,
#                                action=f"/area/restrita/{icao}/ils/{frequency}/edit",
#                                ILSCats=get_ils_categories(),
#                                canDelete=True)
#     else:
#         ident = request.form.get('Ident')
#         runway_head = request.form.get('RunwayHead')
#         frequency_new = request.form.get('Frequency')
#         category = request.form.get('Category')
#         crs = request.form.get('CRS')
#         minimum = request.form.get('Minimum')

#         if (exc := patch_ils(icao=icao,
#                             frequency_old=frequency,
#                             ident=ident,
#                             runway_head=runway_head,
#                             frequency=frequency_new,
#                             category=category,
#                             crs=crs,
#                             minimum=minimum)) is not None:
#             return exc, 401

#         return redirect(f"/area/restrita/{icao}")


# @admin.post("/area/restrita/<string:icao>/ils/<int:frequency>/delete")
# def delete_ils(icao: str, frequency: int):
#     get_logged_user(icao_to_check=icao)
#     del_ils(icao, frequency)
#     return redirect(f"/area/restrita/{icao}")


# @admin.route("/area/restrita/<string:icao>/vor/add", methods=['GET', 'POST'])
# def add_vor(icao: str):
#     get_logged_user(icao_to_check=icao)
#     if request.method == 'GET':
#         vor = {"Ident": "",
#                "Frequency": "",
#               }
#         return render_template("admin/vor.html", icao=icao, vor=vor, action=f"/area/restrita/{icao}/vor/add")
#     else:
#         ident = request.form.get('Ident')
#         frequency = request.form.get('Frequency')

#         if (exc := create_vor(icao=icao,
#                               ident=ident,
#                               frequency=frequency,
#                               )) is not None:
#             return exc, 401

#         return redirect(f"/area/restrita/{icao}")


# @admin.route("/area/restrita/<string:icao>/vor/<int:frequency>/edit", methods=['GET', 'POST'])
# def edit_vor(icao: str, frequency: int):
#     get_logged_user(icao_to_check=icao)
#     if request.method == 'GET':
#         vor = get_vor(icao=icao, frequency=frequency)
#         return render_template("admin/vor.html",
#                                icao=icao,
#                                vor=vor,
#                                action=f"/area/restrita/{icao}/vor/{frequency}/edit",
#                                canDelete=True)
#     else:
#         ident = request.form.get('Ident')
#         frequency_new = request.form.get('Frequency')

#         if (exc := patch_vor(icao=icao,
#                              frequency_old=frequency,
#                              ident=ident,
#                              frequency=frequency_new,
#                              )) is not None:
#             return exc, 401

#         return redirect(f"/area/restrita/{icao}")


# @admin.post("/area/restrita/<string:icao>/vor/<int:frequency>/delete")
# def delete_vor(icao: str, frequency: int):
#     get_logged_user(icao_to_check=icao)
#     del_vor(icao, frequency)
#     return redirect(f"/area/restrita/{icao}")


# @admin.errorhandler(NotLoggedException)
# def not_logged(e):
#     return redirect("/area/restrita/login")


# @admin.errorhandler(NotAllowedToEditAirport)
# def airport_not_allowed(e):
#     return render_template("error.html", "User can't edit this airport")

# @admin.errorhandler(NotSuperUser)
# def no_create_delete_permision(e):
#     return render_template("error.html", "User can't create or remove airports")

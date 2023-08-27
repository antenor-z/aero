import re
from typing import Tuple
from pydantic import BaseModel, constr

class Comm(BaseModel):
    freq: constr(pattern=r'^\d{3}\.\d{3}$') | None = None
    type: str | None = None

class Vor(BaseModel):
    ident: str
    freq: constr(pattern=r'^\d{3}\.\d$')

class Ils(BaseModel):
    rwy: constr(pattern=r'^\d{2}[L|C|R]*$')
    ident: constr(pattern=r'^[A-Z]{3}$')
    freq: constr(pattern=r'^\d{3}\.\d$')
    type: constr(pattern=r'^[I]+$') | None = None
    minimus: constr(pattern=r'^\d+$') | None = None
    crs: constr(pattern=r'^\d{3}$') | None = None
    cat: constr(pattern=r'^[A-Za-z]+$') | None = None

class Rwy(BaseModel):
    head: Tuple[constr(pattern=r'^(\d{2}|\d)(R|L|C)*$'), constr(pattern=r'^(\d{2}|\d)(R|L|C)*$')]
    length: int

class Airport(BaseModel):
    nome: str
    cidade: str
    icao: constr(pattern=r'^[A-Z]{4}$')
    comm: list[Comm] | None = None
    ils: list[Ils] | None = None
    vor: list[Vor] | None = None
    rwy: list[Rwy]

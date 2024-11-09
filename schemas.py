# schemas.py

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, time

class RiverRegister(BaseModel):
    id: int
    register_metadata_id: int
    river_status: str
    site_id: int
    env_temp: float
    cloudiness: str
    wind_status: str
    wind_velocity: float
    precipitation: str
    z: float
    temperature: float
    gauge: float
    area: float
    average_speed: float
    width: float
    hm: float
    observations: str
    ph: float
    conductivity: float
    od: float
    od_percentage: float
    tds: float
    water_temperature: float
    water_odor: str
    water_color: str
    turbidity: float

class RegisterMetadata(BaseModel):
    id: int
    arrival_time: datetime
    departure_time: datetime
    latitude: float
    longitude: float
    observations: str

class Device(BaseModel):
    id: int
    make: str
    model: str
    belonging: str

class DeviceRegisterCrossRef(BaseModel):
    device_id: int
    register_metadata_id: int
    device_category: str

class Persona(BaseModel):
    id: int
    first_name: str
    last_name: str
    dni: str
    affiliation: str

class PersonaRegisterCrossRef(BaseModel):
    persona_id: int
    register_metadata_id: int
    role: str

class Profile(BaseModel):
    id: int
    site_id: int
    code: str
    mix_criteria: str
    mix_description: str
    stratification_criteria: str
    stratification_description: str

class Sample(BaseModel):
    id: int
    number: int
    time: datetime
    register_metadata_id: int
    profile_id: int
    observations: str

class Site(BaseModel):
    id: int
    site: str
    abbreviation: str

class Vegetation(BaseModel):
    id: int
    name: str
    context: str

class VegetationRegisterCrossRef(BaseModel):
    river_register_id: int
    vegetation_id: int

class RiverRegisterRequest(BaseModel):
    river_register: RiverRegister
    register_metadata: RegisterMetadata
    devices: List[Device]
    device_register_cross_refs: List[DeviceRegisterCrossRef]
    personas: List[Persona]
    persona_register_cross_refs: List[PersonaRegisterCrossRef]
    profiles: List[Profile]
    samples: List[Sample]
    sites: List[Site]
    vegetations: List[Vegetation]
    vegetation_register_cross_refs: List[VegetationRegisterCrossRef]

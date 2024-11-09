#This file defines Pydantic models (schemas) for request validation and serialization. These schemas correspond to the data structures expected from the mobile app.


# schemas.py

from pydantic import BaseModel  # Import BaseModel from Pydantic for creating data models
from typing import List, Optional  # Import typing utilities
from datetime import datetime, time  # Import datetime and time classes

# Define the RiverRegister schema
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

# Define the RegisterMetadata schema
class RegisterMetadata(BaseModel):
    id: int
    arrival_time: datetime
    departure_time: datetime
    latitude: float
    longitude: float
    observations: str

# Define the Device schema
class Device(BaseModel):
    id: int
    make: str
    model: str
    belonging: str

# Define the DeviceRegisterCrossRef schema
class DeviceRegisterCrossRef(BaseModel):
    device_id: int
    register_metadata_id: int
    device_category: str

# Define the Persona schema
class Persona(BaseModel):
    id: int
    first_name: str
    last_name: str
    dni: str
    affiliation: str

# Define the PersonaRegisterCrossRef schema
class PersonaRegisterCrossRef(BaseModel):
    persona_id: int
    register_metadata_id: int
    role: str

# Define the Profile schema
class Profile(BaseModel):
    id: int
    site_id: int
    code: str
    mix_criteria: str
    mix_description: str
    stratification_criteria: str
    stratification_description: str

# Define the Sample schema
class Sample(BaseModel):
    id: int
    number: int
    time: datetime
    register_metadata_id: int
    profile_id: int
    observations: str

# Define the Site schema
class Site(BaseModel):
    id: int
    site: str
    abbreviation: str

# Define the Vegetation schema
class Vegetation(BaseModel):
    id: int
    name: str
    context: str  # Context can be 'SHORE' or 'WATER'

# Define the VegetationRegisterCrossRef schema
class VegetationRegisterCrossRef(BaseModel):
    river_register_id: int
    vegetation_id: int

# Define the main request schema for RiverRegister
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

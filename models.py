#This file defines the SQLAlchemy ORM models that map to the PostgreSQL database tables. Each class corresponds to a table in the database schema.

# models.py

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Time, Numeric
from sqlalchemy.orm import relationship  # Import relationship to define relationships between models
from database import Base  # Import the declarative base from database.py

# Define the WaterBody model representing the water_body table
class WaterBody(Base):
    __tablename__ = 'water_body'
    __table_args__ = {'schema': 'monitoring_schema_v3'}  # Specify the schema name

    id = Column(Integer, primary_key=True)
    water_body_name = Column(String(255))

# Define the Site model representing the site table
class Site(Base):
    __tablename__ = 'site'
    __table_args__ = {'schema': 'monitoring_schema_v3'}

    id = Column(Integer, primary_key=True)
    site = Column(String)
    water_body_id = Column(Integer, ForeignKey('monitoring_schema_v3.water_body.id'))
    water_body = relationship('WaterBody', backref='sites')

# Define the Weather model representing the weather table
class Weather(Base):
    __tablename__ = 'weather'
    __table_args__ = {'schema': 'monitoring_schema_v3'}

    id = Column(Integer, primary_key=True)
    env_temp = Column(Float)
    cloudiness = Column(String)
    wind_status = Column(String)
    wind_velocity = Column(Float)
    precipitation = Column(String)

# Define the RiverGauge model representing the river_gauge table
class RiverGauge(Base):
    __tablename__ = 'river_gauge'
    __table_args__ = {'schema': 'monitoring_schema_v3'}

    id = Column(Integer, primary_key=True)
    gauge = Column(Float)
    area = Column(Float)
    average_speed = Column(Float)
    width = Column(Float)
    hm = Column(Float)
    observations = Column(String)

# Define the Monitoring model representing the monitoring table
class Monitoring(Base):
    __tablename__ = 'monitoring'
    __table_args__ = {'schema': 'monitoring_schema_v3'}

    id = Column(Integer, primary_key=True)
    number = Column(Integer)
    date = Column(DateTime)
    season = Column(String)
    hydrological_year = Column(String)

# Define the RecordMetadata model representing the record_metadata table
class RecordMetadata(Base):
    __tablename__ = 'record_metadata'
    __table_args__ = {'schema': 'monitoring_schema_v3'}

    id = Column(Integer, primary_key=True)
    monitoring_id = Column(Integer, ForeignKey('monitoring_schema_v3.monitoring.id'))
    weather_id = Column(Integer, ForeignKey('monitoring_schema_v3.weather.id'))
    arrival_time = Column(DateTime)
    departure_time = Column(DateTime)
    latitude = Column(Float)
    longitude = Column(Float)
    observations = Column(String)

    monitoring = relationship('Monitoring', backref='record_metadata')
    weather = relationship('Weather', backref='record_metadata')

# Define the RiverMetadata model representing the river_metadata table
class RiverMetadata(Base):
    __tablename__ = 'river_metadata'
    __table_args__ = {'schema': 'monitoring_schema_v3'}

    id = Column(Integer, primary_key=True)
    record_metadata_id = Column(Integer, ForeignKey('monitoring_schema_v3.record_metadata.id'), unique=True)
    river_status = Column(String)
    river_gauge_id = Column(Integer, ForeignKey('monitoring_schema_v3.river_gauge.id'))
    water_color = Column(String)
    site_id = Column(Integer, ForeignKey('monitoring_schema_v3.site.id'))

    record_metadata = relationship('RecordMetadata', backref='river_metadata')
    river_gauge = relationship('RiverGauge', backref='river_metadata')
    site = relationship('Site', backref='river_metadata')

# Define the Device model representing the device table
class Device(Base):
    __tablename__ = 'device'
    __table_args__ = {'schema': 'monitoring_schema_v3'}

    id = Column(Integer, primary_key=True)
    make = Column(String)
    model = Column(String)
    belonging = Column(String)

# Define the DeviceRecordMetadata model representing the device_record_metadata table
class DeviceRecordMetadata(Base):
    __tablename__ = 'device_record_metadata'
    __table_args__ = {'schema': 'monitoring_schema_v3'}

    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey('monitoring_schema_v3.device.id'))
    record_metadata_id = Column(Integer, ForeignKey('monitoring_schema_v3.record_metadata.id'))
    device_category = Column(String)

    device = relationship('Device', backref='device_record_metadata')
    record_metadata = relationship('RecordMetadata', backref='device_record_metadata')

# Define the Persona model representing the persona table
class Persona(Base):
    __tablename__ = 'persona'
    __table_args__ = {'schema': 'monitoring_schema_v3'}

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    dni = Column(String)
    affiliation = Column(String)

# Define the PersonaRecordMetadata model representing the persona_record_metadata table
class PersonaRecordMetadata(Base):
    __tablename__ = 'persona_record_metadata'
    __table_args__ = {'schema': 'monitoring_schema_v3'}

    id = Column(Integer, primary_key=True)
    persona_id = Column(Integer, ForeignKey('monitoring_schema_v3.persona.id'))
    record_metadata_id = Column(Integer, ForeignKey('monitoring_schema_v3.record_metadata.id'))
    role = Column(String)

    persona = relationship('Persona', backref='persona_record_metadata')
    record_metadata = relationship('RecordMetadata', backref='persona_record_metadata')

# Define the Profile model representing the profile table
class Profile(Base):
    __tablename__ = 'profile'
    __table_args__ = {'schema': 'monitoring_schema_v3'}

    id = Column(Integer, primary_key=True)
    site_id = Column(Integer, ForeignKey('monitoring_schema_v3.site.id'))
    code = Column(String, unique=True)
    mix_criteria = Column(String)
    mix_description = Column(String)
    stratification_criteria = Column(String)
    stratification_description = Column(String)

    site = relationship('Site', backref='profiles')

# Define the Record model representing the record table
class Record(Base):
    __tablename__ = 'record'
    __table_args__ = {'schema': 'monitoring_schema_v3'}

    id = Column(Integer, primary_key=True)
    depth = Column(Float)
    record_metadata_id = Column(Integer, ForeignKey('monitoring_schema_v3.record_metadata.id'))

    record_metadata = relationship('RecordMetadata', backref='records')

# Define the Sample model representing the sample table
class Sample(Base):
    __tablename__ = 'sample'
    __table_args__ = {'schema': 'monitoring_schema_v3'}

    id = Column(Integer, primary_key=True)
    number = Column(Integer)
    time = Column(Time)
    record_id = Column(Integer, ForeignKey('monitoring_schema_v3.record.id'))
    profile_id = Column(Integer, ForeignKey('monitoring_schema_v3.profile.id'))
    observations = Column(String)
    laboratory = Column(String)

    record = relationship('Record', backref='samples')
    profile = relationship('Profile', backref='samples')

# Define the ShoreVegetation model representing the shore_vegetation table
class ShoreVegetation(Base):
    __tablename__ = 'shore_vegetation'
    __table_args__ = {'schema': 'monitoring_schema_v3'}

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

# Define the WaterVegetation model representing the water_vegetation table
class WaterVegetation(Base):
    __tablename__ = 'water_vegetation'
    __table_args__ = {'schema': 'monitoring_schema_v3'}

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

# Define the RiverShoreVegetation model representing the river_shore_vegetation table
class RiverShoreVegetation(Base):
    __tablename__ = 'river_shore_vegetation'
    __table_args__ = {'schema': 'monitoring_schema_v3'}

    id = Column(Integer, primary_key=True)
    river_metadata_id = Column(Integer, ForeignKey('monitoring_schema_v3.river_metadata.id'))
    shore_vegetation_id = Column(Integer, ForeignKey('monitoring_schema_v3.shore_vegetation.id'))

    river_metadata = relationship('RiverMetadata', backref='river_shore_vegetations')
    shore_vegetation = relationship('ShoreVegetation', backref='river_shore_vegetations')

# Define the RiverWaterVegetation model representing the river_water_vegetation table
class RiverWaterVegetation(Base):
    __tablename__ = 'river_water_vegetation'
    __table_args__ = {'schema': 'monitoring_schema_v3'}

    id = Column(Integer, primary_key=True)
    river_metadata_id = Column(Integer, ForeignKey('monitoring_schema_v3.river_metadata.id'))
    water_vegetation_id = Column(Integer, ForeignKey('monitoring_schema_v3.water_vegetation.id'))

    river_metadata = relationship('RiverMetadata', backref='river_water_vegetations')
    water_vegetation = relationship('WaterVegetation', backref='river_water_vegetations')

# app.py

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from models import Base
import schemas

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/river_register/")
def create_river_register(request: schemas.RiverRegisterRequest, db: Session = Depends(get_db)):
    # Save weather data
    weather = models.Weather(
        env_temp=request.river_register.env_temp,
        cloudiness=request.river_register.cloudiness,
        wind_status=request.river_register.wind_status,
        wind_velocity=request.river_register.wind_velocity,
        precipitation=request.river_register.precipitation
    )
    db.add(weather)
    db.commit()
    db.refresh(weather)

    # Save monitoring data (Assuming monitoring data is provided or defaulted)
    monitoring = models.Monitoring(number=1, date=request.register_metadata.arrival_time)
    db.add(monitoring)
    db.commit()
    db.refresh(monitoring)

    # Save register_metadata
    register_metadata = models.RecordMetadata(
        monitoring_id=monitoring.id,
        weather_id=weather.id,
        arrival_time=request.register_metadata.arrival_time,
        departure_time=request.register_metadata.departure_time,
        latitude=request.register_metadata.latitude,
        longitude=request.register_metadata.longitude,
        observations=request.register_metadata.observations
    )
    db.add(register_metadata)
    db.commit()
    db.refresh(register_metadata)

    # Save RiverGauge data
    river_gauge = models.RiverGauge(
        gauge=request.river_register.gauge,
        area=request.river_register.area,
        average_speed=request.river_register.average_speed,
        width=request.river_register.width,
        hm=request.river_register.hm,
        observations=request.river_register.observations
    )
    db.add(river_gauge)
    db.commit()
    db.refresh(river_gauge)

    # Save RiverMetadata
    river_metadata = models.RiverMetadata(
        record_metadata_id=register_metadata.id,
        river_status=request.river_register.river_status,
        river_gauge_id=river_gauge.id,
        water_color=request.river_register.water_color,
        site_id=request.river_register.site_id
    )
    db.add(river_metadata)
    db.commit()
    db.refresh(river_metadata)

    # Save devices and device_record_metadata
    for device_data in request.devices:
        device = db.query(models.Device).filter_by(id=device_data.id).first()
        if not device:
            device = models.Device(
                id=device_data.id,
                make=device_data.make,
                model=device_data.model,
                belonging=device_data.belonging
            )
            db.add(device)
            db.commit()
            db.refresh(device)

    for cross_ref in request.device_register_cross_refs:
        device_record_metadata = models.DeviceRecordMetadata(
            device_id=cross_ref.device_id,
            record_metadata_id=register_metadata.id,
            device_category=cross_ref.device_category
        )
        db.add(device_record_metadata)
    db.commit()

    # Save personas and persona_record_metadata
    for persona_data in request.personas:
        persona = db.query(models.Persona).filter_by(id=persona_data.id).first()
        if not persona:
            persona = models.Persona(
                id=persona_data.id,
                first_name=persona_data.first_name,
                last_name=persona_data.last_name,
                dni=persona_data.dni,
                affiliation=persona_data.affiliation
            )
            db.add(persona)
            db.commit()
            db.refresh(persona)

    for cross_ref in request.persona_register_cross_refs:
        persona_record_metadata = models.PersonaRecordMetadata(
            persona_id=cross_ref.persona_id,
            record_metadata_id=register_metadata.id,
            role=cross_ref.role
        )
        db.add(persona_record_metadata)
    db.commit()

    # Save profiles
    for profile_data in request.profiles:
        profile = db.query(models.Profile).filter_by(id=profile_data.id).first()
        if not profile:
            profile = models.Profile(
                id=profile_data.id,
                site_id=profile_data.site_id,
                code=profile_data.code,
                mix_criteria=profile_data.mix_criteria,
                mix_description=profile_data.mix_description,
                stratification_criteria=profile_data.stratification_criteria,
                stratification_description=profile_data.stratification_description
            )
            db.add(profile)
    db.commit()

    # Save samples
    for sample_data in request.samples:
        record = models.Record(
            depth=request.river_register.z,
            record_metadata_id=register_metadata.id
        )
        db.add(record)
        db.commit()
        db.refresh(record)

        sample = models.Sample(
            number=sample_data.number,
            time=sample_data.time.time(),
            record_id=record.id,
            profile_id=sample_data.profile_id,
            observations=sample_data.observations
        )
        db.add(sample)
    db.commit()

    # Save vegetations
    for vegetation_data in request.vegetations:
        if vegetation_data.context == "SHORE":
            vegetation = db.query(models.ShoreVegetation).filter_by(name=vegetation_data.name).first()
            if not vegetation:
                vegetation = models.ShoreVegetation(name=vegetation_data.name)
                db.add(vegetation)
                db.commit()
                db.refresh(vegetation)
        elif vegetation_data.context == "WATER":
            vegetation = db.query(models.WaterVegetation).filter_by(name=vegetation_data.name).first()
            if not vegetation:
                vegetation = models.WaterVegetation(name=vegetation_data.name)
                db.add(vegetation)
                db.commit()
                db.refresh(vegetation)

    # Save vegetation cross refs
    for cross_ref in request.vegetation_register_cross_refs:
        vegetation_data = next((v for v in request.vegetations if v.id == cross_ref.vegetation_id), None)
        if vegetation_data.context == "SHORE":
            shore_vegetation = db.query(models.ShoreVegetation).filter_by(name=vegetation_data.name).first()
            river_shore_vegetation = models.RiverShoreVegetation(
                river_metadata_id=river_metadata.id,
                shore_vegetation_id=shore_vegetation.id
            )
            db.add(river_shore_vegetation)
        elif vegetation_data.context == "WATER":
            water_vegetation = db.query(models.WaterVegetation).filter_by(name=vegetation_data.name).first()
            river_water_vegetation = models.RiverWaterVegetation(
                river_metadata_id=river_metadata.id,
                water_vegetation_id=water_vegetation.id
            )
            db.add(river_water_vegetation)
    db.commit()

    return {"message": "River register created successfully"}
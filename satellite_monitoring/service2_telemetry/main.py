from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
import random
import math

app = FastAPI(title="Satellite Telemetry Service", version="1.0.0")

# CORS para permitir o frontend em localhost:8080
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuração do banco de dados SQLite (para teste)
DATABASE_URL = "sqlite:///./satellite_telemetry.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelo SQLAlchemy para Telemetria
class Telemetry(Base):
    __tablename__ = "telemetry"
    
    id = Column(Integer, primary_key=True, index=True)
    satellite_id = Column(Integer, index=True)
    satellite_name = Column(String(100), index=True)
    temperature = Column(Float)  # Temperatura em Celsius
    battery_level = Column(Float)  # Nível de bateria em porcentagem
    latitude = Column(Float)  # Latitude
    longitude = Column(Float)  # Longitude
    altitude = Column(Float)  # Altitude em km
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    

Base.metadata.create_all(bind=engine)

# Modelos Pydantic
class TelemetryResponse(BaseModel):
    id: int
    satellite_id: int
    satellite_name: str
    temperature: float
    battery_level: float
    latitude: float
    longitude: float
    altitude: float
    timestamp: datetime
    
    class Config:
        from_attributes = True

# Dependência para obter sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def generate_telemetry_data(satellite_id: int, satellite_name: str):
    """Gera dados simulados de telemetria para um satélite (versão original)."""
    time_factor = datetime.utcnow().timestamp() / 3600  # Horas desde epoch
    if satellite_name == "Hubble Space Telescope":
        altitude = 540 + random.uniform(-10, 10)
        latitude = 28.5 * math.sin(time_factor * 0.1) + random.uniform(-2, 2)
        longitude = (time_factor * 15) % 360 + random.uniform(-5, 5)
        base_temp = 20
        base_battery = 85
    elif satellite_name == "ISS (International Space Station)":
        altitude = 408 + random.uniform(-5, 5)
        latitude = 51.6 * math.sin(time_factor * 0.08) + random.uniform(-1, 1)
        longitude = (time_factor * 12) % 360 + random.uniform(-3, 3)
        base_temp = 25
        base_battery = 90
    else:  # NOAA-19
        altitude = 870 + random.uniform(-15, 15)
        latitude = 90 * math.sin(time_factor * 0.05) + random.uniform(-3, 3)
        longitude = (time_factor * 8) % 360 + random.uniform(-2, 2)
        base_temp = 15
        base_battery = 75

    return {
        "satellite_id": satellite_id,
        "satellite_name": satellite_name,
        "temperature": base_temp + random.uniform(-5, 5),
        "battery_level": max(0, min(100, base_battery + random.uniform(-3, 3))),
        "latitude": max(-90, min(90, latitude)),
        "longitude": longitude % 360,
        "altitude": max(0, altitude),
        "timestamp": datetime.utcnow(),
    }

def initialize_telemetry_data(db: Session):
    """Inicializa dados de telemetria para todos os satélites"""
    satellites = [
        {"id": 1, "name": "Hubble Space Telescope"},
        {"id": 2, "name": "ISS (International Space Station)"},
        {"id": 3, "name": "NOAA-19"}
    ]
    
    for sat in satellites:
        # Gerar dados históricos (últimas 24 horas)
        for i in range(24):
            timestamp = datetime.utcnow().replace(
                hour=(datetime.utcnow().hour - i) % 24,
                minute=random.randint(0, 59),
                second=random.randint(0, 59)
            )
            
            telemetry_data = generate_telemetry_data(sat["id"], sat["name"])
            telemetry_data["timestamp"] = timestamp
            
            telemetry = Telemetry(**telemetry_data)
            db.add(telemetry)
    
    db.commit()

# Rotas
@app.get("/")
def read_root():
    return {"message": "Satellite Telemetry Service is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "satellite_telemetry"}

@app.get("/telemetry", response_model=List[TelemetryResponse])
def get_all_telemetry(limit: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):
    """Retorna dados de telemetria de todos os satélites"""
    try:
        # Inicializar dados se necessário
        if db.query(Telemetry).count() == 0:
            initialize_telemetry_data(db)
        
        # Gerar novos dados para todos os satélites
        satellite_names = {
            1: "Hubble Space Telescope",
            2: "ISS (International Space Station)",
            3: "NOAA-19"
        }
        
        for sat_id, sat_name in satellite_names.items():
            new_telemetry_data = generate_telemetry_data(sat_id, sat_name)
            new_telemetry = Telemetry(**new_telemetry_data)
            db.add(new_telemetry)
        
        db.commit()
        
        # Retornar dados recentes de todos os satélites
        telemetry_data = db.query(Telemetry).order_by(
            Telemetry.timestamp.desc()
        ).limit(limit).all()
        
        return telemetry_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar telemetria: {str(e)}")

@app.get("/telemetria/{satellite_id}", response_model=List[TelemetryResponse])
def get_telemetry(satellite_id: int, limit: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):
    """Dados em tempo real do satélite"""
    try:
        # Inicializar dados se necessário
        if db.query(Telemetry).count() == 0:
            initialize_telemetry_data(db)
        
        # Gerar novo dado de telemetria (versão original)
        satellite_names = {
            1: "Hubble Space Telescope",
            2: "ISS (International Space Station)",
            3: "NOAA-19"
        }
        
        if satellite_id not in satellite_names:
            raise HTTPException(status_code=404, detail="Satélite não encontrado")
        
        # Adicionar novo registro baseado na simulação original
        new_telemetry_data = generate_telemetry_data(satellite_id, satellite_names[satellite_id])
        new_telemetry = Telemetry(**new_telemetry_data)
        db.add(new_telemetry)
        db.commit()
        
        # Retornar dados recentes
        telemetry_data = db.query(Telemetry).filter(
            Telemetry.satellite_id == satellite_id
        ).order_by(Telemetry.timestamp.desc()).limit(limit).all()
        
        return telemetry_data
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar telemetria: {str(e)}")

@app.get("/telemetria/{satellite_id}/ultimo", response_model=TelemetryResponse)
def get_latest_telemetry(satellite_id: int, db: Session = Depends(get_db)):
    """Último dado coletado do satélite"""
    try:
        # Inicializar dados se necessário
        if db.query(Telemetry).count() == 0:
            initialize_telemetry_data(db)
        
        # Gerar novo dado de telemetria (versão original)
        satellite_names = {
            1: "Hubble Space Telescope",
            2: "ISS (International Space Station)",
            3: "NOAA-19"
        }
        
        if satellite_id not in satellite_names:
            raise HTTPException(status_code=404, detail="Satélite não encontrado")
        
        # Adicionar novo registro baseado na simulação original
        new_telemetry_data = generate_telemetry_data(satellite_id, satellite_names[satellite_id])
        new_telemetry = Telemetry(**new_telemetry_data)
        db.add(new_telemetry)
        db.commit()
        
        # Retornar último registro
        latest_telemetry = db.query(Telemetry).filter(
            Telemetry.satellite_id == satellite_id
        ).order_by(Telemetry.timestamp.desc()).first()
        
        if not latest_telemetry:
            raise HTTPException(status_code=404, detail="Dados de telemetria não encontrados")
        
        return latest_telemetry
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar telemetria: {str(e)}")

@app.get("/telemetria/{satellite_id}/historico", response_model=List[TelemetryResponse])
def get_telemetry_history(
    satellite_id: int, 
    limit: int = Query(10, ge=1, le=100), 
    db: Session = Depends(get_db)
):
    """Histórico de dados de telemetria"""
    try:
        # Inicializar dados se necessário
        if db.query(Telemetry).count() == 0:
            initialize_telemetry_data(db)
        
        satellite_names = {
            1: "Hubble Space Telescope",
            2: "ISS (International Space Station)",
            3: "NOAA-19"
        }
        
        if satellite_id not in satellite_names:
            raise HTTPException(status_code=404, detail="Satélite não encontrado")
        
        # Retornar histórico
        telemetry_data = db.query(Telemetry).filter(
            Telemetry.satellite_id == satellite_id
        ).order_by(Telemetry.timestamp.desc()).limit(limit).all()
        
        return telemetry_data
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar histórico: {str(e)}")

# --- fim versão original ---

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)

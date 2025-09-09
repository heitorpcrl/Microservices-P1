from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Float
from sqlalchemy.engine import URL
import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import random
import time

app = FastAPI(title="Satellite Status Service", version="1.0.0")

# CORS para permitir o frontend em localhost:8080
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuração do banco de dados SQLite (para teste)
DATABASE_URL = "sqlite:///./satellite_status.db"
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelo SQLAlchemy para Satélites
class Satellite(Base):
    __tablename__ = "satellites"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    status = Column(Boolean, default=True)  # True = ativo, False = inativo
    orbit_type = Column(String(50))
    operational_time = Column(Float)  # Tempo em funcionamento em horas
    last_update = Column(DateTime, default=datetime.utcnow)

# Criar tabelas automaticamente (idempotente)
Base.metadata.create_all(bind=engine)

# Modelos Pydantic
class SatelliteResponse(BaseModel):
    id: int
    name: str
    status: bool
    orbit_type: str
    operational_time: float
    last_update: datetime
    
    class Config:
        from_attributes = True

# Dependência para obter sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Função para simular dados de satélites
def initialize_satellites(db: Session):
    """Inicializa os dados dos satélites se não existirem"""
    if db.query(Satellite).count() == 0:
        satellites_data = [
            {
                "name": "Hubble Space Telescope",
                "status": True,
                "orbit_type": "Low Earth Orbit",
                "operational_time": 120000.0  # ~13.7 anos
            },
            {
                "name": "ISS (International Space Station)",
                "status": True,
                "orbit_type": "Low Earth Orbit",
                "operational_time": 175200.0  # ~20 anos
            },
            {
                "name": "NOAA-19",
                "status": True,
                "orbit_type": "Polar Orbit",
                "operational_time": 87600.0  # ~10 anos
            }
        ]
        
        for sat_data in satellites_data:
            satellite = Satellite(**sat_data)
            db.add(satellite)
        
        db.commit()

# Função para simular mudanças de status
def simulate_status_changes(db: Session):
    """Simula mudanças aleatórias no status dos satélites"""
    satellites = db.query(Satellite).all()
    for satellite in satellites:
        # Mantém o status atual (sem alternância aleatória)
        # satellite.status permanece inalterado

        # Atualizar tempo operacional (adicionar algumas horas)
        satellite.operational_time += random.uniform(0.1, 0.5)
        satellite.last_update = datetime.utcnow()
    
    db.commit()

# Rotas
@app.get("/")
def read_root():
    return {"message": "Satellite Status Service is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "satellite_status"}

@app.get("/satelites", response_model=list[SatelliteResponse])
def get_satellites(db: Session = Depends(get_db)):
    """Lista todos os satélites"""
    try:
        # Inicializar dados se necessário
        initialize_satellites(db)
        
        # Simular mudanças de status
        simulate_status_changes(db)
        
        satellites = db.query(Satellite).all()
        return satellites
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar satélites: {str(e)}")

@app.get("/satelites/{satellite_id}", response_model=SatelliteResponse)
def get_satellite(satellite_id: int, db: Session = Depends(get_db)):
    """Retorna dados de um satélite específico"""
    try:
        # Inicializar dados se necessário
        initialize_satellites(db)
        
        # Simular mudanças de status
        simulate_status_changes(db)
        
        satellite = db.query(Satellite).filter(Satellite.id == satellite_id).first()
        if satellite is None:
            raise HTTPException(status_code=404, detail="Satélite não encontrado")
        
        return satellite
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar satélite: {str(e)}")

@app.get("/satelites/name/{satellite_name}", response_model=SatelliteResponse)
def get_satellite_by_name(satellite_name: str, db: Session = Depends(get_db)):
    """Retorna dados de um satélite pelo nome"""
    try:
        # Inicializar dados se necessário
        initialize_satellites(db)
        
        # Simular mudanças de status
        simulate_status_changes(db)
        
        satellite = db.query(Satellite).filter(Satellite.name == satellite_name).first()
        if satellite is None:
            raise HTTPException(status_code=404, detail="Satélite não encontrado")
        
        return satellite
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar satélite: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

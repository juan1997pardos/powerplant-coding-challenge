from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict
import json
from datetime import datetime

from models import ProductionLog
from database import Base, engine, SessionLocal

from sqlalchemy.exc import SQLAlchemyError

app = FastAPI()
Base.metadata.create_all(bind=engine)

class FuelInfo(BaseModel):
    gas: float
    kerosine: float
    co2: float
    wind: float

class PowerPlant(BaseModel):
    name: str
    type: str
    efficiency: float
    pmin: float
    pmax: float

class ProductionPlanRequest(BaseModel):
    load: float
    fuels: Dict[str, float]
    powerplants: List[PowerPlant]

class PowerAllocation(BaseModel):
    name: str
    p: float
    cost: float

@app.post("/productionplan", response_model=List[PowerAllocation])
async def production_plan(payload: ProductionPlanRequest, request: Request):
    session = SessionLocal()
    raw_body = await request.body()
    request_data = json.loads(raw_body)
    try:
        payload = ProductionPlanRequest(**request_data)
        load = payload.load
        fuels = payload.fuels
        plants = []

        for plant in payload.powerplants:
            if plant.type == "windturbine":
                cost = 0
                available_pmax = plant.pmax * fuels["wind(%)"] / 100
            elif plant.type == "gasfired":
                cost = (fuels["gas(euro/MWh)"] / plant.efficiency) + (0.3 * fuels["co2(euro/ton)"])
                available_pmax = plant.pmax
            elif plant.type == "turbojet":
                cost = (fuels["kerosine(euro/MWh)"] / plant.efficiency) + (0.3 * fuels["co2(euro/ton)"])
                available_pmax = plant.pmax
            else:
                raise HTTPException(status_code=400, detail=f"Unknown plant type: {plant.type}")

            plants.append({
                "name": plant.name,
                "type": plant.type,
                "pmin": plant.pmin,
                "pmax": available_pmax,
                "cost": cost
            })

        plants = sorted(plants, key=lambda x: x["cost"])
        remaining_load = load
        response = []

        for plant in plants:
            available_pmin = plant["pmin"]
            available_pmax = plant["pmax"]

            if remaining_load <= 0:
                production = 0
            else:
                production = min(available_pmax, remaining_load)
                if production < available_pmin:
                    production = 0
                elif production > remaining_load:
                    production = remaining_load

            rounded_production = round(production, 1)
            total_cost = round(rounded_production * plant["cost"], 2)

            response.append({
                "name": plant["name"],
                "p": rounded_production,
                "cost": total_cost
            })
            remaining_load -= rounded_production

        if remaining_load > 0:
            raise HTTPException(status_code=400, detail="Load cannot be met with available powerplants.")
        
        total_cost_value = sum(item["cost"] for item in response)
        total_load_value = sum(item["p"] for item in response)
        
        # Save successful log
        log = ProductionLog(
            request_payload=json.dumps(request_data),
            total_load= total_load_value,
            total_cost= total_cost_value,
            response_payload= json.dumps(response),
            error=None
        )
        session.add(log)
        session.commit()

        return response

    except Exception as e:
        # Save error log
        session.add(ProductionLog(
            request_payload=json.dumps(request_data),
            response_payload="[]",
            error=str(e)
        ))
        session.commit()
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        session.close()
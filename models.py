from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from datetime import datetime
from database import Base

class ProductionLog(Base):
    __tablename__ = "production_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.now)
    request_payload = Column(Text)
    total_load = Column(Float)
    total_cost = Column(Float)
    response_payload = Column(Text)
    error = Column(Text)

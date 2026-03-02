
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import Base, engine, SessionLocal
from .models import ConsentCurrent

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Unified Consent Management Platform")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
def health():
    return {"status": "UCMP Running"}

@app.get("/consent/{user_id}")
def get_current(user_id: str, db: Session = Depends(get_db)):
    return db.query(ConsentCurrent).filter(
        ConsentCurrent.user_id == user_id
    ).all()

from fastapi import FastAPI, status, Depends, HTTPException
import models
from routes import router, authentication
from config import engine, SessionLocal
from sqlalchemy.orm import Session

# Membuat tabel dalam database (jika belum ada)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Menambahkan rute yang telah Anda definisikan
app.include_router(authentication, tags=["authentication"])
app.include_router(router, prefix="/marilearn", tags=["marilearn"])
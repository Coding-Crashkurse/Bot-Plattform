from fastapi import FastAPI
from app.api import auth, users, bots
from app.database import engine, Base

# Datenbankinitialisierung (falls nötig)
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Routen registrieren mit Präfixen
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(bots.router, prefix="/bots", tags=["bots"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the LLM Platform"}

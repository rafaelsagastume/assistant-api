from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.apikey.routes import router as apikey_router
from src.auth.routes import router as auth_router

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(apikey_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}

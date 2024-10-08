from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.apikey.routes import router as apikey_router
from src.assistants.routes import router as assistants_router
from src.auth.routes import router as auth_router
from src.chat.routes import router as chat_router
from src.credentials.routes import router as credentials_router
from src.functions.routes import router as functions_router

app = FastAPI(
    title="Assistant API",
    description="Empower your business with smart and fast AI-powered responses.",
    version="0.1.0",
)

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
app.include_router(assistants_router)
app.include_router(credentials_router)
app.include_router(functions_router)
app.include_router(chat_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}

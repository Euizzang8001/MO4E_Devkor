from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from config.database import create_tables
from routers import user

create_tables()
app = FastAPI()

app.include_router(user.router)

origins = ["*"]

#어떤 도메인이든, 어떤 헤더이든 다 받아주겠다
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}
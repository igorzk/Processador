from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import parsers

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

app.include_router(parsers.router)


@app.get("/")
async def root():
    return {"message": "Connectivity ok"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

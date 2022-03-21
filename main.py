from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import parsers

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(parsers.router)


@app.get("/")
async def root():
    return {"message": "Hello Jenkins, I hope you are fine"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

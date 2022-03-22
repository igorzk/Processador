from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import parsers

app = FastAPI()

#origins = ["http://localhost", "http://investjs.ik.ntr", "http://localhost:8080", "hptt://localhost:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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

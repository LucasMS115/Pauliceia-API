from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers.geocoding import geocoding_router

origins = ['*']

app = FastAPI(title='Pauliceia API',
              description='Documentation of the Pauliceia\'s API',
              version='0.1')

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(geocoding_router.router)


@app.get("/")
async def root():
    return {"message": "Hello from the Pauliceia\'s API!"}

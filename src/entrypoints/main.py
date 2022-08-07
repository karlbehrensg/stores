from fastapi import FastAPI


from src.entrypoints.routes import countries

app = FastAPI()


app.include_router(countries.router)

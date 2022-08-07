from fastapi import FastAPI


from src.entrypoints.routes import countries, roles

app = FastAPI()


app.include_router(countries.router)
app.include_router(roles.router)

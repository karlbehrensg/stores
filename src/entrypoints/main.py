from fastapi import FastAPI


from src.entrypoints.routes import countries, roles, stores

app = FastAPI()


app.include_router(countries.router)
app.include_router(roles.router)
app.include_router(stores.router)

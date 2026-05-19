from fastapi import FastAPI
from routers import all_routers
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in all_routers:
    app.include_router(router)

@app.get("/")
def root():
    return {"message": "API Posgrado funcionando ✅"}
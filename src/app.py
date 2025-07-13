from src.api.routes import router

from fastapi import FastAPI
    
    
def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(router)

    
    return app
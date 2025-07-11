from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, chat, user
from app.logger import setup_logger
from app.middleware.log_request import LogRequestMiddleware
from fastapi.openapi.utils import get_openapi
from app.routers import admin

setup_logger()

app = FastAPI(
    title="VLU AI Chatbot",
    description="AI tư vấn tuyển sinh và học vụ – Đại học Văn Lang",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,

    allow_origins=["http://localhost:3000","http://127.0.0.1:8000","https://have-suitable-resistance-fitted.trycloudflare.com",],
    # thay bằng link fe sau khi chạy cd frontend cloudflared tunnel --url http://localhost:3000, thay bằng link be sau kho chạy cloudflared tunnel --url http://127.0.0.1:8000
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router, prefix="/auth", tags=["Auth"],)       
app.include_router(chat.router, prefix="/chat", tags=["Chat"])        
app.include_router(user.router, prefix="/users", tags=["Users"])     
app.include_router(admin.router, prefix="/admin",tags=["Admin"])

@app.get("/", tags=["Health"])
async def root():
    return {"message": "VLU Chatbot API is up and running! "}

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "Bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", [{"BearerAuth": []}])

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

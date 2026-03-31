# -*- coding: utf-8 -*-
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from config.settings import settings
from config.database import engine, Base
from routes.auth import router as auth_router

# 自动建表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="用户认证系统 API",
    description="基于 FastAPI + MySQL 的注册登录接口",
    version="1.0.0"
)

# 跨域配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://localhost:8082"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 统一异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"code": 500, "message": "服务器内部错误"}
    )

# 注册路由
app.include_router(auth_router, prefix="/api")

# 健康检查
@app.get("/api/health", tags=["系统"])
def health_check():
    return {"code": 200, "message": "Server is running!"}


if __name__ == "__main__":
    print(f"🚀 服务器启动成功，监听端口: {settings.PORT}")
    print(f"📝 API 文档地址: http://localhost:{settings.PORT}/docs")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=True
    )

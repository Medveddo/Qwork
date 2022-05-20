import logging

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from starlette_exporter import PrometheusMiddleware, handle_metrics

from app.endpoints import endpoints_router
from app.utils import health_check_app

load_dotenv()


class EndpointFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.args and len(record.args) >= 3 and record.args[2] not in ("/metrics", "/health")


logging.getLogger("uvicorn.access").addFilter(EndpointFilter())

app = FastAPI(
    title="QworkAPI",
    description=(
        "REST API of web application responible for extracting structured "
        "data from text and checking text corresonding "
        "to clinical recomendations "
    ),
    version="0.1.2",
    contact={
        "name": "Sizikov Vitaly",
        "url": "https://vk.com/vitaliksiz",
        "email": "sizikov.vitaly@gmail.com",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", handle_metrics)
app.include_router(endpoints_router)


@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Warming up the engines 🧑‍🚀 ...")
    app_healthy = await health_check_app()
    if not app_healthy:
        raise Exception("Startup healthcheck failed")
    logger.info("💥 Database and Redis are healthy 💥 !")


@app.on_event("shutdown")
def shutdown_event():
    logger.info("🌇 Bye bye, Sir 🎩 ...")

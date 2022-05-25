import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from loguru import logger
from sqlalchemy.orm import Session

import app.tasks as tasks
from app import crud, schemas
from app.database import get_db
from app.hashids import hashids_
from app.nlp.services.controller import controller_service
from app.utils import health_check_app

endpoints_router = APIRouter()


@endpoints_router.get(
    "/stats",
    tags=["Text process"],
    summary="Returns total runs count and match percentage",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {"texts_processed_total": 7, "corresponding_runs_percent": 0.6666666666666666}
                }
            },
        }
    },
)
async def stats(db: Session = Depends(get_db)):
    total_runs, correspod_part = crud.get_runs_stat(db)
    return {
        "texts_processed_total": total_runs,
        "corresponding_runs_percent": correspod_part,
    }


@endpoints_router.get(
    "/health",
    summary="Enpoint for checking if API is available",
    tags=["Service enpoints"],
)
async def health(response: Response):
    app_healthy = await health_check_app()
    if not app_healthy:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return False

    return True


@endpoints_router.get(
    "/now",
    tags=["Service enpoints"],
    summary="Returns current server UTC time",
    responses={
        200: {
            "content": {
                "application/json": {"example": {"time": "2022-05-23T15:32:51.767488"}},
            }
        },
    },
)
async def now(request: Request):
    return {"time": datetime.datetime.utcnow()}


@endpoints_router.get(
    "/run/{hashid}",
    tags=["Text process"],
    summary="Get text processing result",
)
async def get_run(
    request: Request,
    hashid: str,
    response: Response,
    db: Session = Depends(get_db),
) -> schemas.Run:
    db_run_id = hashids_.from_hash_id(hashid)
    if not db_run_id:
        raise HTTPException(status_code=404, detail="Run not found")

    logger.debug(f"Get run #{db_run_id}")
    run = crud.get_run(db, db_run_id)
    if not run:
        response.status_code = status.HTTP_404_NOT_FOUND
        return
    logger.debug(f"Run: {run}")

    if not run.finished:
        response.status_code = status.HTTP_202_ACCEPTED
        processing_run = schemas.ProcessingRun(run_id=hashid, finished=False)
        logger.debug(f"Run still processing: {processing_run}")
        return processing_run

    logger.success(run)
    return run


@endpoints_router.post(
    "/process_text_instant",
    tags=["Text process"],
    summary="Instattly returns the result of finding features",
    description=(
        "Instattly returns the result of finding features corresponding to :type in :text"
        "Request-response endpoint with pending connection. "
        "Recomended to use '/process_text' enpoint that returns run_id "
        "then result can be retrieved at '/run_result/<run_id>'"
    ),
    response_model=schemas.FeaturesResult,
)
async def process_text_instant(request: Request, input: schemas.TextInput, db: Session = Depends(get_db)):
    logger.debug(f"process_text_instant - input: {input}")
    run = crud.create_run_new(db, input)
    result = controller_service.process_text_with_related_clinrecs(input)
    logger.debug(f"process_text_instant - output: {result}")
    crud.update_run_result(db, run.id, result)
    # crud.save_text_and_find_result(db, input.text, result)
    return result


@endpoints_router.post(
    "/process_text",
    tags=["Text process"],
    summary="Start processing text run in backgorund",
    description=(
        "Instatly gives you hash_id of your run. " "After that you can get a result with /run/{hashid} endpoint"
    ),
    response_model=schemas.ResponseWithRunId,
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "run_id": "095zpx3ZdYMLwGkZ",
                    }
                }
            },
        }
    },
)
async def process_text(
    request: Request,
    response: Response,
    input: schemas.TextInput,
    db: Session = Depends(get_db),
) -> schemas.ResponseWithRunId:
    logger.debug(f"Input text: {input}")

    run = crud.create_run_new(db, input)

    task = tasks.process_run.send(run.id)
    logger.debug(f"Start background processing task {task}")

    response.status_code = status.HTTP_202_ACCEPTED
    return {"run_id": hashids_.to_hash_id(run.id)}


@endpoints_router.get(
    "/history",
    tags=["Text process"],
    summary="Get runs history",
    response_model=List[schemas.RunNew],
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": [
                        {
                            "text": "Температура 37.9. Давление высокое - 120 на 80.",
                            "type": "all",
                            "result": {
                                "found_features": ["Температура", "Артериальное давление"],
                                "missing_features": [
                                    "Частота сердечных сокращений",
                                    "Электрокардиограмма (ЭКГ)",
                                    "Фибрилляция пердсердий",
                                    "Общий анализ крови",
                                    "Вес",
                                    "Рост",
                                    "Индекс массы тела",
                                ],
                            },
                            "finished": True,
                            "run_id": None,
                        }
                    ]
                }
            },
        }
    },
)
def read_history(
    request: Request,
    count: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    results = crud.get_new_runs_history(db, count, offset)
    logger.debug(f"{results=}")
    return results


@endpoints_router.get(
    "/dramatiq",
    tags=["Service enpoints"],
    summary="Healthcheck dramatiq task processor",
    responses={
        200: {
            "content": {
                "application/json": {"example": "2022-05-23 15:31:26.838184 I'm fine!"},
            }
        },
    },
)
def dramatiq(request: Request):
    tasks.say_something()
    message = tasks.say_something.send()
    return message.get_result(block=True)

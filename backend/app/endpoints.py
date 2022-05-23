import datetime

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


@endpoints_router.get("/stats")
async def stats(db: Session = Depends(get_db)):
    total_runs, correspod_part = crud.get_runs_stat(db)
    return {
        "texts_processed_total": total_runs,
        "corresponding_runs_percent": correspod_part,
    }


@endpoints_router.get("/health")
async def health(response: Response):
    app_healthy = await health_check_app()
    if not app_healthy:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return False

    return True


@endpoints_router.get(
    "/now",
    tags=["Service enpoints"],
    summary="Please fill me",
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
    logger.debug(f"Run: {run}")
    if not run.finished:
        response.status_code = status.HTTP_202_ACCEPTED
        processing_run = schemas.ProcessingRun(run_id=hashid, finished=False)
        logger.debug(f"Run still processing: {processing_run}")
        return

    logger.success(run)
    return run


@endpoints_router.post(
    "/process_text_instant",
    tags=["Text process"],
    summary="Please fill me",
    description=(
        "Request-response endpoint with pending connection. "
        "Recomended to use '/process_text' enpoint that returns run_id "
        "then result can be retrieved at '/run_result/<run_id>'"
    ),
)
async def process_text_instant(request: Request, input: schemas.TextInput, db: Session = Depends(get_db)):
    logger.debug(f"process_text_instant - input: {input}")
    result = controller_service.process_text_with_related_clinrecs(input)
    logger.debug(f"process_text_instant - output: {result}")
    crud.save_text_and_find_result(db, input.text, result)
    return result


@endpoints_router.post(
    "/process_text",
    tags=["Text process"],
    summary="Please fill me",
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

    run = crud.create_run(db, input)

    task = tasks.process_run.send(run.id)
    logger.debug(f"Start background processing task {task}")

    response.status_code = status.HTTP_202_ACCEPTED
    return {"run_id": hashids_.to_hash_id(run.id)}


@endpoints_router.get(
    "/history",
    tags=["Text process"],
    summary="Get runs history",
    # response_model=list[schemas.Run],
    # responses={
    #     200: {
    #         "content": {
    #             "application/json": {
    #                 "example": [
    #                     {
    #                         "text": "Температура 37.9. Давление высокое - 120 на 80.",  # noqa
    #                         "is_correspond": True,
    #                         "temperature": 37.9,
    #                         "systole_pressure": 120,
    #                         "diastole_pressure": 80,
    #                         "run_id": "095zpx3ZdYMLwGkZ",
    #                     }
    #                 ]
    #             }
    #         },
    #     }
    # },
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
    summary="Please fill me",
)
def dramatiq(request: Request):
    tasks.say_something()
    message = tasks.say_something.send()
    return message.get_result(block=True)

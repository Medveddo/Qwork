import datetime

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from sqlalchemy.orm import Session
from starlette_exporter import PrometheusMiddleware, handle_metrics

from app import crud, models, schemas
from app.database import SessionLocal, engine
from app.nlp import verify_temp_and_blood_pressure
from app.tasks import say_something

load_dotenv()


_, _ = models, engine
# models.Base.metadata.create_all(bind=engine)

origins = [
    "*",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", handle_metrics)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/now")
async def now(request: Request):
    return {"time": datetime.datetime.utcnow()}


@app.post("/process_text")
async def process_text(
    request: Request, input: schemas.TextInput, db: Session = Depends(get_db)
):
    logger.debug(f"Input text: {input}")

    result = verify_temp_and_blood_pressure(input.text)

    result_ = schemas.Run(
        text=input.text,
        is_corresponding=result.is_correspond,
        temperature=result.temperature,
        systole_pressure=result.systole_pressure,
        diastole_pressure=result.diastole_pressure,
    )
    logger.debug(f"{result_=}")

    crud.create_text_process_result(db, result_)

    result_dict = {
        "is_correspond": "❌",
        "temperature": "",
        "systole_pressure": "",
        "diastole_pressure": "",
    }

    if result.is_correspond:
        result_dict.update({"is_correspond": "✅"})
    if result.temperature:
        result_dict.update({"temperature": result.temperature})
    if result.systole_pressure:
        result_dict.update({"systole_pressure": result.systole_pressure})
    if result.diastole_pressure:
        result_dict.update({"diastole_pressure": result.diastole_pressure})

    logger.debug(result_dict)
    return result_dict


@app.get("/history", response_model=list[schemas.Run])
def read_history(request: Request, db: Session = Depends(get_db)):
    results = crud.get_history(db)
    logger.debug(f"{results=}")
    return results


@app.get("/dramatiq")
def dramatiq(request: Request):
    say_something()
    say_something.send()
    return "Ok!"

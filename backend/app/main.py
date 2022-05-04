import datetime
from typing import List

from dotenv import load_dotenv
from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    Request,
    WebSocket,
    WebSocketDisconnect,
)
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from sqlalchemy.orm import Session
from starlette_exporter import PrometheusMiddleware, handle_metrics

from app import crud, models, schemas
from app.database import SessionLocal, engine
from app.hashids import hashids_
from app.nlp import verify_temp_and_blood_pressure

import app.tasks as tasks

load_dotenv()


_, _ = models, engine
# models.Base.metadata.create_all(bind=engine)

origins = [
    "*",
]

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
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", handle_metrics)


def get_db():
    logger.debug("Creating session to DB ...")
    db = SessionLocal()
    try:
        yield db
    finally:
        logger.debug("Closing session to DB ...")
        db.close()


@app.get(
    "/now",
    tags=["Service enpoints"],
    summary="Please fill me",
)
async def now(request: Request):
    return {"time": datetime.datetime.utcnow()}


@app.get(
    "/run/{hashid}",
    tags=["Text process"],
    summary="Get text processing result",
)
async def get_run(request: Request, hashid: str):
    db_id = hashids_.from_hash_id(hashid)
    if not db_id:
        raise HTTPException(status_code=404, detail="Run not found")
    try:
        db = SessionLocal()
        run: models.Run = db.query(models.Run).get(db_id)
        run.show_info()
        return 200
    finally:
        db.close()


@app.post(
    "/process_text_instant",
    tags=["Text process"],
    summary="Please fill me",
    description=(
        "Request-response endpoint with pending connection. "
        "Recomended to use '/process_text' enpoint that returns run_id "
        "then result can be retrieved at '/run_result/<run_id>'"
    ),
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "is_correspond": True,
                        "temperature": 37.9,
                        "systole_pressure": 120,
                        "diastole_pressure": 80,
                        "run_id": "095zpx3ZdYMLwGkZ",
                    }
                }
            },
        }
    },
    response_model=schemas.RunResult,
)
async def process_text_instant(
    request: Request, input: schemas.TextInput, db: Session = Depends(get_db)
) -> schemas.RunResult:
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

    run = crud.create_text_process_result(db, result_)

    run_result = schemas.RunResult(run_id=hashids_.to_hash_id(run.id))

    if result.is_correspond:
        run_result.is_correspond = True
    if result.temperature:
        run_result.temperature = result.temperature
    if result.systole_pressure:
        run_result.systole_pressure = result.systole_pressure
    if result.diastole_pressure:
        run_result.diastole_pressure = result.diastole_pressure

    logger.debug(run_result.json())
    return run_result


@app.post(
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
    request: Request, input: schemas.TextInput, db: Session = Depends(get_db)
) -> schemas.ResponseWithRunId:
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

    run = crud.create_text_process_result(db, result_)

    result_dict = {
        "is_correspond": "❌",
        "temperature": "",
        "systole_pressure": "",
        "diastole_pressure": "",
        "run_id": hashids_.to_hash_id(run.id),
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


@app.get(
    "/history",
    tags=["Text process"],
    summary="Get runs history",
    response_model=list[schemas.Run],
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": [{
                        "text": "Температура 37.9. Давление высокое - 120 на 80.",
                        "is_correspond": True,
                        "temperature": 37.9,
                        "systole_pressure": 120,
                        "diastole_pressure": 80,
                        "run_id": "095zpx3ZdYMLwGkZ",
                    }]
                }
            },
        }
    },
)
def read_history(request: Request, db: Session = Depends(get_db)):
    results = crud.get_history(db)
    logger.debug(f"{results=}")
    return results


@app.get(
    "/dramatiq",
    tags=["Service enpoints"],
    summary="Please fill me",
)
def dramatiq(request: Request):
    tasks.say_something()
    tasks.say_something.send()
    tasks.process_run(1)
    return "Ok!"


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.websocket(
    "/ws",
)
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"ws: got data: {data}")
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@app.get(
    "/websocket",
    tags=["Service enpoints"],
    summary="Please fill me",
)
async def sock():
    html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""
    return HTMLResponse(html)

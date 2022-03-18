import datetime

from fastapi import Depends, FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
origins = [
    "*",
]

from sqlalchemy.orm import Session

from loguru import logger
from .database import SessionLocal, engine

from .nlp import verify_temp_and_blood_pressure

from . import crud, models, schemas

_, _ = models, engine
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
async def process_text(request: Request, input: schemas.TextInput, db: Session = Depends(get_db)):
    logger.debug(f"Input text: {input}")
    

    result = verify_temp_and_blood_pressure(input.text)
    
    result_ = schemas.TextProcessResult(
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

@app.get("/history", response_model=list[schemas.TextProcessResult])
def read_history(request: Request, db: Session = Depends(get_db)):
    results = crud.get_history(db)
    logger.debug(f"{results=}")
    return results

# @app.post("/users/", response_model=schemas.User)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_email(db, email=user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return crud.create_user(db=db, user=user)


# @app.get("/users/", response_model=list[schemas.User])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users


# @app.get("/users/{user_id}", response_model=schemas.User)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user


# @app.post("/users/{user_id}/items/", response_model=schemas.Item)
# def create_item_for_user(
#     user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)


# @app.get("/items/", response_model=list[schemas.Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items

from sqlalchemy.orm import Session

from . import models, schemas

from loguru import logger

def get_history(db: Session):
    logger.info("Fetching all results from db")
    results: list[models.TextProcessResult] = db.query(models.TextProcessResult).all()
    logger.info(f"{results=}")
    return [
        schemas.TextProcessResult(
            text=result.text, 
            is_corresponding=result.is_corresponding,
            temperature=result.temperature,
            systole_pressure=result.systole_pressure,
            diastole_pressure=result.diastole_pressure,
        ) for result in results
    ]
    

def create_text_process_result(db: Session, result: schemas.TextProcessResult):
    db_result = models.TextProcessResult(**result.dict())
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result


# def get_user(db: Session, user_id: int):
#     return db.query(models.User).filter(models.User.id == user_id).first()


# def get_user_by_email(db: Session, email: str):
#     return db.query(models.User).filter(models.User.email == email).first()


# def get_users(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.User).offset(skip).limit(limit).all()


# def create_user(db: Session, user: schemas.UserCreate):
#     fake_hashed_password = user.password + "notreallyhashed"
#     db_user = models.User(
#         email=user.email, hashed_password=fake_hashed_password
#     )
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user


# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()


# def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
#     db_item = models.Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item

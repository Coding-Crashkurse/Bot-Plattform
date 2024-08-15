from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.crud import bot as crud_bot
from app.crud import user as crud_user
from app import schemas
from app.database import get_db
from fastapi.responses import JSONResponse

router = APIRouter()


@router.post("/", response_model=schemas.Group, status_code=status.HTTP_201_CREATED)
def create_group(group: schemas.GroupCreate, db: Session = Depends(get_db)):
    db_group = crud_bot.get_group_by_name(db, name=group.name)
    if db_group:
        raise HTTPException(status_code=400, detail="Group already registered")
    return crud_bot.create_group(db=db, group=group)


@router.get("/", response_model=List[schemas.Group])
def read_groups(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    groups = crud_bot.get_groups(db, skip=skip, limit=limit)
    return groups


@router.get("/{group_id}", response_model=schemas.Group)
def read_group(group_id: int, db: Session = Depends(get_db)):
    group = crud_bot.get_group(db=db, group_id=group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return group


@router.put("/{group_id}", response_model=schemas.Group)
def update_group(
    group_id: int, group: schemas.GroupCreate, db: Session = Depends(get_db)
):
    db_group = crud_bot.get_group(db=db, group_id=group_id)
    if not db_group:
        raise HTTPException(status_code=404, detail="Group not found")
    db_group.name = group.name
    db.commit()
    db.refresh(db_group)
    return db_group


@router.delete("/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_group(group_id: int, db: Session = Depends(get_db)):
    group = crud_bot.get_group(db=db, group_id=group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    db.delete(group)
    db.commit()
    return {"message": "Group deleted successfully"}


@router.post("/{group_id}/assign-user/", response_model=schemas.Group)
def assign_user_to_group(group_id: int, user_id: int, db: Session = Depends(get_db)):
    group = crud_bot.get_group(db=db, group_id=group_id)
    user = crud_user.get_user(db=db, user_id=user_id)

    if not group or not user:
        raise HTTPException(status_code=404, detail="Group or user not found")

    if user in group.users:
        return JSONResponse(
            status_code=status.HTTP_208_ALREADY_REPORTED,
            content={
                "message": "User is already assigned to this group",
                "group": schemas.Group.model_validate(
                    group, from_attributes=True
                ).model_dump(),
            },
        )

    group.users.append(user)
    db.commit()
    db.refresh(group)

    group_data = schemas.Group.model_validate(group, from_attributes=True).model_dump()
    return group_data


@router.post("/{group_id}/assign-bot/", response_model=schemas.Group)
def assign_bot_to_group(group_id: int, bot_id: int, db: Session = Depends(get_db)):
    group = crud_bot.assign_bot_to_group(db=db, group_id=group_id, bot_id=bot_id)

    if not group:
        raise HTTPException(status_code=404, detail="Group or bot not found")

    group_data = schemas.Group.model_validate(group, from_attributes=True).model_dump()
    return group_data


@router.get("/{group_id}/users/", response_model=List[schemas.UserEmailIdSchema])
def read_users_in_group(group_id: int, db: Session = Depends(get_db)):
    users = crud_bot.get_users_in_group(db=db, group_id=group_id)
    if users is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return users


@router.get("/{group_id}/bots/", response_model=List[schemas.BotIdNameSchema])
def read_bots_in_group(group_id: int, db: Session = Depends(get_db)):
    bots = crud_bot.get_bots_in_group(db=db, group_id=group_id)
    if bots is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return bots

from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.schemas import TagModel, TagResponse
from src.repository import tags as repository_tags
from src.services.auth import auth_service

router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("/", response_model=List[TagResponse])
async def read_tags(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    tags = await repository_tags.get_tags(skip, limit, current_user, db)
    return tags


@router.get("/{tag_id}", response_model=TagResponse)
async def read_tag(
    tag_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    tag = await repository_tags.get_tag(tag_id, current_user, db)
    if tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found"
        )
    return tag


@router.post("/", response_model=TagResponse, status_code=status.HTTP_201_CREATED)
async def create_tag(
    body: TagModel,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    return await repository_tags.create_tag(body, current_user, db)


@router.put("/{tag_id}", response_model=TagResponse)
async def update_tag(
    body: TagModel,
    tag_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    tag = await repository_tags.update_tag(tag_id, body, current_user, db)
    if tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found"
        )
    return tag


@router.delete("/{tag_id}", response_model=TagResponse)
async def remove_tag(
    tag_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    tag = await repository_tags.remove_tag(tag_id, current_user, db)
    if tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found"
        )
    return tag

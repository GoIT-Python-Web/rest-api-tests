from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import and_

from src.database.models import Tag, User
from src.schemas import TagModel


async def get_tags(skip: int, limit: int, user: User, db: Session) -> List[Tag]:
    """
    Retrieve all tags that belong to a specific user.

    :param skip: The number of records to skip.
    :type skip: int
    :param limit: The maximum number of records to retrieve.
    :type limit: int
    :param user: The user object that owns the tags.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: A list of Tag objects.
    :rtype: List[Tag]
    """
    return db.query(Tag).filter(Tag.user_id == user.id).offset(skip).limit(limit).all()


async def get_tag(tag_id: int, user: User, db: Session) -> Tag:
    """
    Retrieve a specific tag that belongs to a user.

    :param tag_id: The ID of the tag to retrieve.
    :type tag_id: int
    :param user: The user object that owns the tag.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The Tag object with the specified ID.
    :rtype: Tag
    """
    return db.query(Tag).filter(and_(Tag.id == tag_id, Tag.user_id == user.id)).first()


async def create_tag(body: TagModel, user: User, db: Session) -> Tag:
    """
    Create a new tag for a user.

    :param body: The attributes of the new tag.
    :type body: TagModel
    :param user: The user object that will own the new tag.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The newly created Tag object.
    :rtype: Tag
    """
    tag = Tag(name=body.name, user_id=user.id)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


async def update_tag(
    tag_id: int, body: TagModel, user: User, db: Session
) -> Tag | None:
    """
    Update an existing tag that belongs to a user.

    :param tag_id: The ID of the tag to update.
    :type tag_id: int
    :param body: The new attributes of the tag.
    :type body: TagModel
    :param user: The user object that owns the tag.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The updated Tag object.
    :rtype: Tag | None
    """
    tag = db.query(Tag).filter(and_(Tag.id == tag_id, Tag.user_id == user.id)).first()
    if tag:
        tag.name = body.name
        db.commit()
    return tag


async def remove_tag(tag_id: int, user: User, db: Session) -> Tag | None:
    """
    Remove a tag that belongs to a user.

    :param tag_id: The ID of the tag to remove.
    :type tag_id: int
    :param user: The user object that owns the tag.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The Tag object that was removed.
    :rtype: Tag | None
    """
    tag = db.query(Tag).filter(and_(Tag.id == tag_id, Tag.user_id == user.id)).first()
    if tag:
        db.delete(tag)
        db.commit()
    return tag

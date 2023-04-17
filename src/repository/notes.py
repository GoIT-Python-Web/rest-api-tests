from typing import List

from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.database.models import Note, Tag, User
from src.schemas import NoteModel, NoteUpdate, NoteStatusUpdate


async def get_notes(skip: int, limit: int, user: User, db: Session) -> List[Note]:
    """
    Retrieves a list of notes for a specific user with specified pagination parameters.

    :param skip: The number of notes to skip.
    :type skip: int
    :param limit: The maximum number of notes to return.
    :type limit: int
    :param user: The user to retrieve notes for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: A list of notes.
    :rtype: List[Note]
    """
    return (
        db.query(Note).filter(Note.user_id == user.id).offset(skip).limit(limit).all()
    )


async def get_note(note_id: int, user: User, db: Session) -> Note:
    """
    Retrieves a single note with the specified ID for a specific user.

    :param note_id: The ID of the note to retrieve.
    :type note_id: int
    :param user: The user to retrieve the note for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The note with the specified ID, or None if it does not exist.
    :rtype: Note | None
    """
    return (
        db.query(Note).filter(and_(Note.id == note_id, Note.user_id == user.id)).first()
    )


async def create_note(body: NoteModel, user: User, db: Session) -> Note:
    """
    Creates a new note for a specific user.

    :param body: The data for the note to create.
    :type body: NoteModel
    :param user: The user to create the note for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The newly created note.
    :rtype: Note
    """
    tags = (
        db.query(Tag).filter(and_(Tag.id.in_(body.tags), Tag.user_id == user.id)).all()
    )
    note = Note(title=body.title, description=body.description, tags=tags, user=user)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


async def remove_note(note_id: int, user: User, db: Session) -> Note | None:
    """
    Removes a single note with the specified ID for a specific user.

    :param note_id: The ID of the note to remove.
    :type note_id: int
    :param user: The user to remove the note for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The removed note, or None if it does not exist.
    :rtype: Note | None
    """
    note = (
        db.query(Note).filter(and_(Note.id == note_id, Note.user_id == user.id)).first()
    )
    if note:
        db.delete(note)
        db.commit()
    return note


async def update_note(
    note_id: int, body: NoteUpdate, user: User, db: Session
) -> Note | None:
    """
    Updates a single note with the specified ID for a specific user.

    :param note_id: The ID of the note to update.
    :type note_id: int
    :param body: The updated data for the note.
    :type body: NoteUpdate
    :param user: The user to update the note for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The updated note, or None if it does not exist.
    :rtype: Note | None
    """
    note = (
        db.query(Note).filter(and_(Note.id == note_id, Note.user_id == user.id)).first()
    )
    if note:
        tags = (
            db.query(Tag)
            .filter(and_(Tag.id.in_(body.tags), Note.user_id == user.id))
            .all()
        )
        note.title = body.title
        note.description = body.description
        note.done = body.done
        note.tags = tags
        db.commit()
    return note


async def update_status_note(
    note_id: int, body: NoteStatusUpdate, user: User, db: Session
) -> Note | None:
    """
    Updates the status (i.e. "done" or "not done") of a single note with the specified ID for a specific user.

    :param note_id: The ID of the note to update.
    :type note_id: int
    :param body: The updated status for the note.
    :type body: NoteStatusUpdate
    :param user: The user to update the note for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The updated note, or None if it does not exist.
    :rtype: Note | None
    """
    note = (
        db.query(Note).filter(and_(Note.id == note_id, Note.user_id == user.id)).first()
    )
    if note:
        note.done = body.done
        db.commit()
    return note

from app import db, FlashcardType, Flashcard

"""
flask shell
from helpers import *
flash_type_count()
"""

def flash_type_count():
    flashcard_types = FlashcardType.query.all()
    for flashcard_type in flashcard_types:
        flashcard_count = Flashcard.query.filter_by(flashcard_type_id=flashcard_type.id).count()
        print(f"Flashcard Type: {flashcard_type.name} | Flashcard Count: {flashcard_count}")

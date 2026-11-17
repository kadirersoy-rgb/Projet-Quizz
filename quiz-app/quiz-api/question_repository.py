import sqlite3
from pathlib import Path

from question_model import Question


DB_PATH = Path(__file__).resolve().parent / "quiz.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def insert_question(cursor, question: Question):
    cursor.execute(
        """
        INSERT INTO questions (position, title, text, image)
        VALUES (?, ?, ?, ?)
        """,
        (
            question.position,
            question.title,
            question.text,
            question.image
        )
    )

    question.id = cursor.lastrowid
    return question


def row_to_question(row):
    return Question(
        id=row["id"],
        position=row["position"],
        title=row["title"],
        text=row["text"],
        image=row["image"]
    )
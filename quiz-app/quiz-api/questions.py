import sqlite3
from pathlib import Path
from question_model import Question

DB_PATH = Path(__file__).resolve().parent / "quiz.db"


def add_question(question: Question):
    connection = sqlite3.connect(DB_PATH)

    try:
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM questions")
        count = cursor.fetchone()[0]

        position = question.position

        if position is None:
            position = count + 1

        if not isinstance(position, int) or isinstance(position, bool):
            raise ValueError("Invalid position")

        if position < 1 or position > count + 1:
            raise ValueError("Invalid position")

        cursor.execute(
            "SELECT id FROM questions WHERE position >= ? ORDER BY position DESC",
            (position,)
        )
        ids_to_shift = [row[0] for row in cursor.fetchall()]

        for question_id in ids_to_shift:
            cursor.execute(
                "UPDATE questions SET position = -position WHERE id = ?",
                (question_id,)
            )

        for question_id in ids_to_shift:
            cursor.execute(
                "UPDATE questions SET position = -position + 1 WHERE id = ?",
                (question_id,)
            )

        cursor.execute(
            """
            INSERT INTO questions (position, title, text, image)
            VALUES (?, ?, ?, ?)
            """,
            (position, question.title, question.text, question.image)
        )

        question.id = cursor.lastrowid
        question.position = position

        connection.commit()

        return question.id

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()
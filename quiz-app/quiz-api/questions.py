
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "quiz.db"


def add_question(title, text, image, position):
    connection = sqlite3.connect(DB_PATH)

    try:
        cursor = connection.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM questions"
        )
        count = cursor.fetchone()[0]

        # Si aucune position n'est fournie, ajouter à la fin
        if position is None:
            position = count + 1

        # Vérifier que la position est valide
        if not isinstance(position, int) or isinstance(position, bool):
            raise ValueError("Invalid position")

        if position < 1 or position > count + 1:
            raise ValueError("Invalid position")

        # Décaler les questions existantes si nécessaire
        cursor.execute(
            "SELECT id FROM questions WHERE position >= ? ORDER BY position DESC",
            (position,)
        )
        ids_to_shift = [row[0] for row in cursor.fetchall()]

        # Décalage temporaire pour éviter les conflits UNIQUE
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
            (position, title, text, image)
        )

        question_id = cursor.lastrowid
        connection.commit()

        return question_id

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()
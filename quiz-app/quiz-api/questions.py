from question_model import Question
from question_repository import get_connection, insert_question


def add_question(question: Question):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("BEGIN")

        cursor.execute("SELECT COUNT(*) FROM questions")
        count = cursor.fetchone()[0]

        position = question.position

        if position is None:
            position = count + 1

        if not isinstance(position, int) or isinstance(position, bool):
            raise ValueError("Invalid position")

        if position < 1 or position > count + 1:
            raise ValueError("Invalid position")

        # Récupérer les questions à décaler
        cursor.execute(
            """
            SELECT id
            FROM questions
            WHERE position >= ?
            ORDER BY position DESC
            """,
            (position,)
        )

        ids_to_shift = [row["id"] for row in cursor.fetchall()]

        # Positions temporaires négatives pour éviter
        # les conflits avec la contrainte UNIQUE
        for question_id in ids_to_shift:
            cursor.execute(
                """
                UPDATE questions
                SET position = -position
                WHERE id = ?
                """,
                (question_id,)
            )

        # Repositionner les questions décalées
        for question_id in ids_to_shift:
            cursor.execute(
                """
                UPDATE questions
                SET position = -position + 1
                WHERE id = ?
                """,
                (question_id,)
            )

        question.position = position

        # Insertion via notre interface Modèle-BDD
        insert_question(cursor, question)

        connection.commit()

        return question.id

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()
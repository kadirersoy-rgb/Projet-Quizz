
from question_model import Question


def json_to_question(data: dict) -> Question:
    return Question(
        title=data["title"],
        text=data["text"],
        image=data.get("image"),
        position=data.get("position"),
        id=data.get("id")
    )


def question_to_json(question: Question) -> dict:
    return {
        "id": question.id,
        "title": question.title,
        "text": question.text,
        "image": question.image,
        "position": question.position
    }
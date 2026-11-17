class Question:
    def __init__(
        self,
        title: str,
        text: str,
        image: str | None = None,
        position: int | None = None,
        id: int | None = None
    ):
        self.id = id
        self.title = title
        self.text = text
        self.image = image
        self.position = position

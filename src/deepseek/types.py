from typing import TypedDict, NotRequired


class Result(TypedDict):
    grade: NotRequired[str]
    description: str
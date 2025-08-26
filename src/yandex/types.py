from typing import TypedDict, Optional, NotRequired


class Result(TypedDict):
    grade: NotRequired[str]
    description: str


class Message(TypedDict):
    role: str
    text: str

class Alternative(TypedDict):
    message: Message
    status: str

class Usage(TypedDict):
    inputTextTokens: str
    completionTokens: str
    totalTokens: str
    completionTokensDetails: Optional[str] 

class AIResult(TypedDict):
    alternatives: list[Alternative]
    usage: Usage
    modelVersion: str

class Response(TypedDict):
    result: AIResult
from pydantic import BaseModel


# Defining request body
class AskRequest(BaseModel):
    question: str
    

# Defining response body
class AskResponse(BaseModel):
    answer: str
    metadata: list
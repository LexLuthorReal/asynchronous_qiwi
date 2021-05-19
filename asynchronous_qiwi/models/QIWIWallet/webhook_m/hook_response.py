from pydantic import BaseModel, Field


class HookResponse(BaseModel):

    response: str = Field(..., alias="response")

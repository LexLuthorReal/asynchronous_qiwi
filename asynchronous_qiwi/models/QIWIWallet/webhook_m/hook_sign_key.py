from pydantic import BaseModel, Field


class HookSignKey(BaseModel):

    key: str = Field(..., alias="key")

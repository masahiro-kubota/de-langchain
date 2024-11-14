from abc import ABC
from typing import Any
from pydantic import BaseModel

class Serializable(BaseModel, ABC):
  def __init__(self, *args: Any, **kwargs: Any) -> None:
    super().__init__(*args, **kwargs)



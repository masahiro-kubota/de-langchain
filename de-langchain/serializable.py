from abc import ABC
from typing import Any
from pydantic import BaseModel

class Serializable(BaseModel, ABC):
  # Remove default BaseModel init docstrig
  def __init__(self, *args: Any, **kwargs: Any) -> None:
    """"""
    super().__init__(*args, **kwargs)

  @classmethod
  def is_lc_serializable(cls) -> bool:
    # TODO implement to_json method
    return False



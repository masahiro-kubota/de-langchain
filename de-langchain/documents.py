from typing import Optional

from pydantic import Field

from de-langchain.serializable import Serializable

class BaseMedia(Serializable)
  id: Optional[str] = None
  metadata: dict = Field(default_factory=dict)

class Document(BaseMedia):
  page_content: str
  type: Literal["Document"] = "Document"
  
  def __init__(self, page_content: str, **kwargs: Any) -> None:
    super().__init__(page_content=page_contentm **kwargs)

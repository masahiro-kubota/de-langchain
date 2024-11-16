from abc import ABC
from collections.abc import Iterator

from de-langchain.documents import Document

class BaseLoader(ABC):
  def load(self) -> list[Document]:
    return list(self.lazy_load())

  def lazy_load(self) -> Iterator[Document]:
    # 'load' shoudn't be overridden, but if load is overrided, return 'iter(load())' istead of 'lazy_load'.
    if type(self).load != BaseLoader.load:
      return iter(self.load())
    msg = f"{self.__class__.__name__} does not implement lazy_load()"
    raise NotImplementedError(msg) 

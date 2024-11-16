import csv
from abc import ABC
from io import TextIOWrapper
from pathlib import Path
from typing import Iterator, Optional, Sequence, Union

from delangchain.documents import Document

class BaseLoader(ABC):
  def load(self) -> list[Document]:
    return list(self.lazy_load())

  def lazy_load(self) -> Iterator[Document]:
    # 'load' shoudn't be overridden, but if load is overrided, return 'iter(load())' istead of 'lazy_load'.
    if type(self).load != BaseLoader.load:
      return iter(self.load())
    msg = f"{self.__class__.__name__} does not implement lazy_load()"
    raise NotImplementedError(msg) 


class CSVLoader(BaseLoader):
  def __init__(
    self,
    file_path: Union[str, Path],
    source_column: Optional[str] = None,
    metadata_columns: Sequence[str] = (),
    encoding: Optional[str] = None,
    csv_args: Optional[dict] = None,
    autodetect_encoding: bool = False,
    *,
    content_columns: Sequence[str] = (),
):
    self.file_path = file_path
    self.source_column = source_column
    self.metadata_columns = metadata_columns
    self.encoding = encoding
    self.csv_args = csv_args or {}
    self.autodetect_encoding = autodetect_encoding
    self.content_columns = content_columns

  def lazy_load(self) -> Iterator[Document]:
    try:
      with open(self.file_path, newline="", encoding=self.encoding) as csvfile:
        yield from self.__read_file(csvfile)
    except Exception as e:
      raise RuntimeError(f"Error loading {self.file_path}") from e

  def __read_file(self, csvfile: TextIOWrapper) -> Iterator[Document]:
    csv_reader = csv.DictReader(csvfile, **self.csv_args)
    for i, row in enumerate(csv_reader):
      source = (
        row[self.source_column]
        if self.source_column is not None
        else str(self.file_path)
      )
      # use generator to reduce memory usage
      content = "\n".join(
        f"""{k.strip() if k is not None else k}: {v.strip()
        if isinstance(v, str) else ','.join(map(str.strip, v))
        if isinstance(v, list) else v}"""
        for k, v in row.items()
        if (
            k in self.content_columns
            if self.content_columns
            else k not in self.metadata_columns
        )
      )
      metadata = {"source": source, "row": i}
      for col in self.metadata_columns:
        try:
          metadata[col] = row[col] 
        except KeyError:
          raise ValueError(f"Metadata column `{col}' not found in CSV file")
      yield Document(page_content=content, metadata=metadata)


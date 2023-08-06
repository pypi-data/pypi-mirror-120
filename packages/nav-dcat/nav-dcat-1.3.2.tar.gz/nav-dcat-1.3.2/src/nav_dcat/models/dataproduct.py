from typing import Optional, Sequence, Union, List
from pydantic import BaseModel

from nav_dcat.fields import common_fields
from nav_dcat.models.dataset import DatasetDocument


class DataproductDocument(BaseModel):
    title: str
    description: str
    repo: str
    pii: common_fields.Pii
    modified: Optional[str] = None
    issued: Optional[str] = None
    periodicity: Optional[str] = ""
    contactPoint: Optional[dict] = {}
    author: Optional[str] = ""
    long_description: Optional[str] = ""
    accessRights: Optional[common_fields.AccessRights] = common_fields.AccessRights.INTERNAL.value
    keyword: Optional[Sequence] = []
    theme: Optional[Union[str, List[str]]] = ""
    temporal: Optional[dict] = {}
    language: Optional[str] = "NO"
    datasets: Optional[List[DatasetDocument]] = []

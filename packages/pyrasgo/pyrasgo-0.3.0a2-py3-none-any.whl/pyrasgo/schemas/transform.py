from datetime import date, datetime
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, TypeVar, Union


class TransformBase(BaseModel):
    name: str
    sourceCode: str
    dimension: Optional[str]


class Transform(TransformBase):
    id: int
    name: str
    sourceCode: str
    arguments: Optional[List]


# POST Transform
class TransformCreate(TransformBase):
    name: str
    sourceCode: str

class ReturnTransformCreate(TransformBase):
    id: int
    arguments: Optional[Dict]

# GET list of transforms
class GetTransformList(BaseModel):
    name: Optional[str]


class Transforms(BaseModel):
    transforms: List[Transform]


# Utilities
class TransformUtilityDefinition(BaseModel):
    name: str
    description: str
    arguments: Dict[str, str]


class TransformUtility(BaseModel):
    name: str
    arguments: Dict[str, str]
    resultArgumentName: str


# POST execute transform
class ExecuteTransform(BaseModel):
    arguments: Optional[Dict[str, str]]
    dimensions: List[str]
    newSourceName: Optional[str]
    dataSourceId: int
    utilities: Optional[List[TransformUtility]]


class ExecuteTransformResponse(BaseModel):
    id: int

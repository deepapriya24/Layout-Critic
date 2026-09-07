from pydantic import BaseModel, Field
from typing import List


class CategoryScore(BaseModel):
    score: float
    note: str


class Categories(BaseModel):
    contrast: CategoryScore
    spacing: CategoryScore
    hierarchy: CategoryScore
    alignment: CategoryScore
    color_harmony: CategoryScore


class Issue(BaseModel):
    label: str
    x: float = Field(..., ge=0, le=1)
    y: float = Field(..., ge=0, le=1)
    w: float = Field(..., ge=0, le=1)
    h: float = Field(..., ge=0, le=1)
    fix: str


class AnalysisResult(BaseModel):
    overall_score: float
    categories: Categories
    issues: List[Issue]


class ErrorResponse(BaseModel):
    error: str

from sqlmodel import SQLModel, Field
from pydantic import BaseModel, Field
from typing import Literal


class UserCreate(SQLModel):
    username: str = Field(min_length=4, max_length=30)
    password: str = Field(min_length=8, max_length=100)


class UserPublic(SQLModel):
    id: int
    username: str


class UserLogin(SQLModel):
    username: str
    password: str



class Token(SQLModel):
    access_token: str
    token_type: str



class PostureBaselineData(SQLModel):
    nose_x: float = Field(ge=0.0, le=1.0)
    nose_y: float = Field(ge=0.0, le=1.0)
    face_box_width: float = Field(ge=0.0, le=1.0)
    face_box_height: float = Field(ge=0.0, le=1.0)


class PostureBaselinePublic(PostureBaselineData):
    id: int
    user_id: int


class CurrentPostureData(PostureBaselineData):
    pass


class PostureComparisonPublic(BaseModel):
    nose_x_error: float
    nose_y_error: float
    face_box_width_error: float
    face_box_height_error: float


class MotorJogRequest(SQLModel):
    axis: Literal[1, 2, 3]
    delta_deg: Literal[1.0, -1.0]



class HomeSaveRequest(SQLModel):
    theta1: float
    theta2: float
    theta3: float


class HomePositionPublic(HomeSaveRequest):
    id: int
    user_id: int
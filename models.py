from sqlmodel import SQLModel, Field
from sqlalchemy import UniqueConstraint

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    hashed_password: str


class HomePosition(SQLModel, table=True):
    __tablename__ = "home_positions"

    __table_args__ = (
        UniqueConstraint("user_id"),
    )

    id: int | None = Field(default=None, primary_key=True)

    user_id: int = Field(
        foreign_key="user.id",
        index=True,
    )

    theta1: float
    theta2: float
    theta3: float
class PostureBaseline(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(
        foreign_key="user.id",
        unique=True,
        index=True,
    )
    nose_x: float
    nose_y: float
    face_box_width: float
    face_box_height: float
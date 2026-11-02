
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Date,
    Float,
    ForeignKey
)
from sqlalchemy.sql import func

from ..database import Base


class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    workout_name = Column(String(100), nullable=False)

    category = Column(String(20), nullable=False)

    duration = Column(Integer, nullable=False)

    calories_burned = Column(Float, nullable=False)

    workout_date = Column(Date, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )


from sqlalchemy import Column, Integer, String, Date, DateTime, Float, ForeignKey
from sqlalchemy.sql import func

from ..database import Base


class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    goal_title = Column(String(100), nullable=False)

    description = Column(String(500), nullable=True)

    target_value = Column(Float, nullable=False)

    current_value = Column(Float, default=0, nullable=False)

    unit = Column(String(30), nullable=False)

    start_date = Column(Date, nullable=False)

    target_date = Column(Date, nullable=False)

    status = Column(
        String(20),
        default="ACTIVE",
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

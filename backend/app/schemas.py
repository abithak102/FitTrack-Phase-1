
from datetime import datetime, date
from typing import Literal

from pydantic import BaseModel, EmailStr, Field, ConfigDict


# -------------------------
# USER SCHEMAS - MODULE 1
# -------------------------

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)


class UserLogin(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: int


# -------------------------
# WORKOUT SCHEMAS - MODULE 2
# -------------------------

class WorkoutCreate(BaseModel):
    workout_name: str = Field(min_length=2, max_length=100)
    category: Literal["Cardio", "Strength", "Yoga"]
    duration: int = Field(gt=0, le=1440)
    calories_burned: float = Field(ge=0, le=10000)
    workout_date: date


class WorkoutUpdate(BaseModel):
    workout_name: str = Field(min_length=2, max_length=100)
    category: Literal["Cardio", "Strength", "Yoga"]
    duration: int = Field(gt=0, le=1440)
    calories_burned: float = Field(ge=0, le=10000)
    workout_date: date


class WorkoutOut(BaseModel):
    id: int
    user_id: int
    workout_name: str
    category: str
    duration: int
    calories_burned: float
    workout_date: date
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

from datetime import date
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, model_validator


class GoalCreate(BaseModel):
    goal_title: str = Field(min_length=2, max_length=100)
    description: str | None = Field(default=None, max_length=500)

    target_value: float = Field(gt=0)
    current_value: float = Field(default=0, ge=0)

    unit: str = Field(min_length=1, max_length=30)

    start_date: date
    target_date: date

    @model_validator(mode="after")
    def validate_goal(self):
        if self.target_date < self.start_date:
            raise ValueError("Target date must be on or after start date.")

        if self.current_value > self.target_value:
            raise ValueError("Current value cannot exceed target value.")

        return self


class GoalUpdate(BaseModel):
    goal_title: str | None = Field(default=None, min_length=2, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    target_value: float | None = Field(default=None, gt=0)
    current_value: float | None = Field(default=None, ge=0)
    unit: str | None = Field(default=None, min_length=1, max_length=30)
    start_date: date | None = None
    target_date: date | None = None
    status: Literal["ACTIVE", "COMPLETED"] | None = None

    model_config = ConfigDict(extra="forbid")


class GoalOut(BaseModel):
    id: int
    user_id: int
    goal_title: str
    description: str | None
    target_value: float
    current_value: float
    unit: str
    start_date: date
    target_date: date
    status: str

    model_config = ConfigDict(from_attributes=True)

from datetime import date
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, model_validator


class GoalCreate(BaseModel):
    goal_title: str = Field(min_length=2, max_length=100)
    description: str | None = Field(default=None, max_length=500)

    target_value: float = Field(gt=0)
    current_value: float = Field(default=0, ge=0)

    unit: str = Field(min_length=1, max_length=30)

    start_date: date
    target_date: date

    @model_validator(mode="after")
    def validate_goal(self):
        if self.target_date < self.start_date:
            raise ValueError("Target date must be on or after start date.")

        if self.current_value > self.target_value:
            raise ValueError("Current value cannot exceed target value.")

        return self


class GoalUpdate(BaseModel):
    goal_title: str | None = Field(default=None, min_length=2, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    target_value: float | None = Field(default=None, gt=0)
    current_value: float | None = Field(default=None, ge=0)
    unit: str | None = Field(default=None, min_length=1, max_length=30)
    start_date: date | None = None
    target_date: date | None = None
    status: Literal["ACTIVE", "COMPLETED"] | None = None

    model_config = ConfigDict(extra="forbid")


class GoalOut(BaseModel):
    id: int
    user_id: int
    goal_title: str
    description: str | None
    target_value: float
    current_value: float
    unit: str
    start_date: date
    target_date: date
    status: str

    model_config = ConfigDict(from_attributes=True)

from datetime import date
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, model_validator


class GoalCreate(BaseModel):
    goal_title: str = Field(min_length=2, max_length=100)
    description: str | None = Field(default=None, max_length=500)

    target_value: float = Field(gt=0)
    current_value: float = Field(default=0, ge=0)

    unit: str = Field(min_length=1, max_length=30)

    start_date: date
    target_date: date

    @model_validator(mode="after")
    def validate_goal(self):
        if self.target_date < self.start_date:
            raise ValueError("Target date must be on or after start date.")

        if self.current_value > self.target_value:
            raise ValueError("Current value cannot exceed target value.")

        return self


class GoalUpdate(BaseModel):
    goal_title: str | None = Field(default=None, min_length=2, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    target_value: float | None = Field(default=None, gt=0)
    current_value: float | None = Field(default=None, ge=0)
    unit: str | None = Field(default=None, min_length=1, max_length=30)
    start_date: date | None = None
    target_date: date | None = None
    status: Literal["ACTIVE", "COMPLETED"] | None = None

    model_config = ConfigDict(extra="forbid")


class GoalOut(BaseModel):
    id: int
    user_id: int
    goal_title: str
    description: str | None
    target_value: float
    current_value: float
    unit: str
    start_date: date
    target_date: date
    status: str

    model_config = ConfigDict(from_attributes=True)
# -------------------------
# USER PROFILE SCHEMAS - MODULE 6
# -------------------------

class UserProfileUpdate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr


class ChangePassword(BaseModel):
    current_password: str = Field(min_length=8, max_length=72)
    new_password: str = Field(min_length=8, max_length=72)
class NotificationCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    message: str = Field(min_length=3, max_length=500)

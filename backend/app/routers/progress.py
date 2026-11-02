
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..database import get_db
from ..models import Workout, User
from ..auth import get_current_user


router = APIRouter(
    prefix="/progress",
    tags=["Progress Tracking"]
)


@router.get("/summary")
def get_progress_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Get total workout count
    total_workouts = db.query(
        func.count(Workout.id)
    ).filter(
        Workout.user_id == current_user.id
    ).scalar() or 0

    # Get total workout duration
    total_duration = db.query(
        func.coalesce(func.sum(Workout.duration), 0)
    ).filter(
        Workout.user_id == current_user.id
    ).scalar()

    # Get total calories burned
    total_calories = db.query(
        func.coalesce(func.sum(Workout.calories_burned), 0)
    ).filter(
        Workout.user_id == current_user.id
    ).scalar()

    # Get category-wise workout count
    category_data = db.query(
        Workout.category,
        func.count(Workout.id).label("count")
    ).filter(
        Workout.user_id == current_user.id
    ).group_by(
        Workout.category
    ).all()

    category_breakdown = [
        {
            "category": category,
            "count": count
        }
        for category, count in category_data
    ]

    return {
        "total_workouts": total_workouts,
        "total_duration": total_duration,
        "total_calories": total_calories,
        "category_breakdown": category_breakdown
    }

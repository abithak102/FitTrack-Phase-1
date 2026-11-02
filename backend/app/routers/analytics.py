
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..database import get_db
from ..models import Workout, User
from ..auth import get_current_user


router = APIRouter(
    prefix="/analytics",
    tags=["Fitness Analytics"]
)


@router.get("/overview")
def get_analytics_overview(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Total workout count
    total_workouts = db.query(
        func.count(Workout.id)
    ).filter(
        Workout.user_id == current_user.id
    ).scalar() or 0

    # Total calories burned
    total_calories = db.query(
        func.coalesce(func.sum(Workout.calories_burned), 0)
    ).filter(
        Workout.user_id == current_user.id
    ).scalar()

    # Total workout duration
    total_duration = db.query(
        func.coalesce(func.sum(Workout.duration), 0)
    ).filter(
        Workout.user_id == current_user.id
    ).scalar()

    # Workout category breakdown
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

    # Monthly workout statistics
    monthly_data = db.query(
        func.strftime("%Y-%m", Workout.workout_date).label("month"),
        func.count(Workout.id).label("workouts"),
        func.coalesce(
            func.sum(Workout.calories_burned), 0
        ).label("calories")
    ).filter(
        Workout.user_id == current_user.id
    ).group_by(
        func.strftime("%Y-%m", Workout.workout_date)
    ).order_by(
        func.strftime("%Y-%m", Workout.workout_date)
    ).all()

    monthly_statistics = [
        {
            "month": month,
            "workouts": workouts,
            "calories": calories
        }
        for month, workouts, calories in monthly_data
    ]

    return {
        "total_workouts": total_workouts,
        "total_calories": total_calories,
        "total_duration": total_duration,
        "category_breakdown": category_breakdown,
        "monthly_statistics": monthly_statistics
    }

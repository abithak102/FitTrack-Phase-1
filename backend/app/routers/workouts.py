
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Workout, User
from ..schemas import WorkoutCreate, WorkoutUpdate, WorkoutOut
from ..auth import get_current_user


router = APIRouter(
    prefix="/workouts",
    tags=["Workouts"]
)


# -------------------------
# CREATE WORKOUT
# -------------------------

@router.post(
    "/",
    response_model=WorkoutOut,
    status_code=status.HTTP_201_CREATED
)
def create_workout(
    workout_data: WorkoutCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_workout = Workout(
        user_id=current_user.id,
        workout_name=workout_data.workout_name,
        category=workout_data.category,
        duration=workout_data.duration,
        calories_burned=workout_data.calories_burned,
        workout_date=workout_data.workout_date
    )

    db.add(new_workout)
    db.commit()
    db.refresh(new_workout)

    return new_workout


# -------------------------
# GET ALL USER WORKOUTS
# -------------------------

@router.get("/", response_model=list[WorkoutOut])
def get_workouts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    workouts = db.query(Workout).filter(
        Workout.user_id == current_user.id
    ).order_by(
        Workout.workout_date.desc()
    ).all()

    return workouts


# -------------------------
# UPDATE WORKOUT
# -------------------------

@router.put("/{workout_id}", response_model=WorkoutOut)
def update_workout(
    workout_id: int,
    workout_data: WorkoutUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    workout = db.query(Workout).filter(
        Workout.id == workout_id,
        Workout.user_id == current_user.id
    ).first()

    if workout is None:
        raise HTTPException(
            status_code=404,
            detail="Workout not found"
        )

    workout.workout_name = workout_data.workout_name
    workout.category = workout_data.category
    workout.duration = workout_data.duration
    workout.calories_burned = workout_data.calories_burned
    workout.workout_date = workout_data.workout_date

    db.commit()
    db.refresh(workout)

    return workout


# -------------------------
# DELETE WORKOUT
# -------------------------

@router.delete(
    "/{workout_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_workout(
    workout_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    workout = db.query(Workout).filter(
        Workout.id == workout_id,
        Workout.user_id == current_user.id
    ).first()

    if workout is None:
        raise HTTPException(
            status_code=404,
            detail="Workout not found"
        )

    db.delete(workout)
    db.commit()

    return None

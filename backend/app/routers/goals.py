
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Goal, User
from ..schemas import GoalCreate, GoalUpdate, GoalOut
from ..auth import get_current_user


router = APIRouter(
    prefix="/goals",
    tags=["Goals Management"]
)


# CREATE GOAL
@router.post("/", response_model=GoalOut, status_code=status.HTTP_201_CREATED)
def create_goal(
    goal_data: GoalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_goal = Goal(
        user_id=current_user.id,
        **goal_data.model_dump()
    )

    db.add(new_goal)
    db.commit()
    db.refresh(new_goal)

    return new_goal


# LIST USER GOALS
@router.get("/", response_model=list[GoalOut])
def get_goals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    goals = db.query(Goal).filter(
        Goal.user_id == current_user.id
    ).order_by(Goal.id.desc()).all()

    return goals


# GET SINGLE GOAL
@router.get("/{goal_id}", response_model=GoalOut)
def get_goal(
    goal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    goal = db.query(Goal).filter(
        Goal.id == goal_id,
        Goal.user_id == current_user.id
    ).first()

    if not goal:
        raise HTTPException(
            status_code=404,
            detail="Goal not found"
        )

    return goal


# UPDATE GOAL
@router.put("/{goal_id}", response_model=GoalOut)
def update_goal(
    goal_id: int,
    goal_data: GoalUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    goal = db.query(Goal).filter(
        Goal.id == goal_id,
        Goal.user_id == current_user.id
    ).first()

    if not goal:
        raise HTTPException(
            status_code=404,
            detail="Goal not found"
        )

    update_data = goal_data.model_dump(exclude_unset=True)

    if "target_value" in update_data:
        new_target = update_data["target_value"]
    else:
        new_target = goal.target_value

    if "current_value" in update_data:
        new_current = update_data["current_value"]
    else:
        new_current = goal.current_value

    if new_current > new_target:
        raise HTTPException(
            status_code=422,
            detail="Current value cannot exceed target value."
        )

    new_start = update_data.get("start_date", goal.start_date)
    new_end = update_data.get("target_date", goal.target_date)

    if new_end < new_start:
        raise HTTPException(
            status_code=422,
            detail="Target date must be on or after start date."
        )

    for key, value in update_data.items():
        setattr(goal, key, value)

    if "current_value" in update_data or "target_value" in update_data:
        if goal.current_value >= goal.target_value:
            goal.status = "COMPLETED"
        elif goal.status == "COMPLETED":
            goal.status = "ACTIVE"

    db.commit()
    db.refresh(goal)

    return goal


# DELETE GOAL
@router.delete("/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_goal(
    goal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    goal = db.query(Goal).filter(
        Goal.id == goal_id,
        Goal.user_id == current_user.id
    ).first()

    if not goal:
        raise HTTPException(
            status_code=404,
            detail="Goal not found"
        )

    db.delete(goal)
    db.commit()

    return None

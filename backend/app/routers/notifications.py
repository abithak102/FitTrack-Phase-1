
from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..auth import get_current_user
from ..models.notification import Notification
from ..models.workout import Workout
from ..schemas import NotificationCreate
from ..models.goal import Goal


router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)


# Create one daily reminder if the user has not worked out today
def create_daily_workout_reminder(db: Session, current_user):

    today = date.today()

    # Check whether the user completed a workout today
    today_workout = (
        db.query(Workout)
        .filter(
            Workout.user_id == current_user.id,
            Workout.workout_date == today
        )
        .first()
    )

    if today_workout:
        return

    # Check whether today's reminder already exists
    existing_reminders = (
        db.query(Notification)
        .filter(
            Notification.user_id == current_user.id,
            Notification.title == "Daily Workout Reminder"
        )
        .all()
    )

    for reminder in existing_reminders:
        if reminder.created_at and reminder.created_at.date() == today:
            return

    # Create a new reminder
    new_reminder = Notification(
        user_id=current_user.id,
        title="Daily Workout Reminder",
        message="You haven't recorded a workout today. Stay active and complete your daily workout!",
        is_read=False
    )

    db.add(new_reminder)
    db.commit()
# Create alerts for completed or overdue goals
def create_goal_progress_alerts(db: Session, current_user):

    today = date.today()

    goals = (
        db.query(Goal)
        .filter(
            Goal.user_id == current_user.id,
            Goal.status == "ACTIVE"
        )
        .all()
    )

    for goal in goals:

        alert_title = None
        alert_message = None

        if goal.current_value >= goal.target_value:

            alert_title = "Goal Completed!"
            alert_message = (
                f"Congratulations! You completed your goal: "
                f"{goal.goal_title}."
            )

        elif goal.target_date < today:

            alert_title = "Goal Deadline Passed"
            alert_message = (
                f"Your goal '{goal.goal_title}' has passed its deadline. "
                "Update your progress and set a new target."
            )

        if alert_title:

            # Avoid duplicate alerts for the same goal and title
            existing_alert = (
                db.query(Notification)
                .filter(
                    Notification.user_id == current_user.id,
                    Notification.title == alert_title,
                    Notification.message == alert_message
                )
                .first()
            )

            if not existing_alert:

                new_notification = Notification(
                    user_id=current_user.id,
                    title=alert_title,
                    message=alert_message,
                    is_read=False
                )

                db.add(new_notification)

    db.commit()

# Create a notification
@router.post("/")
def create_notification(
    notification_data: NotificationCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    new_notification = Notification(
        user_id=current_user.id,
        title=notification_data.title,
        message=notification_data.message,
        is_read=False
    )

    db.add(new_notification)
    db.commit()
    db.refresh(new_notification)

    return {
        "message": "Notification created successfully",
        "notification": new_notification
    }


# Get logged-in user's notifications
@router.get("/")
def get_notifications(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    create_daily_workout_reminder(db, current_user)
    create_goal_progress_alerts(db, current_user)
    create_daily_workout_reminder(db, current_user)
    create_goal_progress_alerts(db, current_user)
    notifications = (
        db.query(Notification)
        .filter(Notification.user_id == current_user.id)
        .order_by(Notification.created_at.desc())
        .all()
    )

    return notifications


# Get unread notification count
@router.get("/unread-count")
def get_unread_count(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    create_daily_workout_reminder(db, current_user)

    count = (
        db.query(Notification)
        .filter(
            Notification.user_id == current_user.id,
            Notification.is_read == False
        )
        .count()
    )

    return {"unread_count": count}


# Mark one notification as read
@router.patch("/{notification_id}/read")
def mark_notification_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    notification = (
        db.query(Notification)
        .filter(
            Notification.id == notification_id,
            Notification.user_id == current_user.id
        )
        .first()
    )

    if not notification:
        raise HTTPException(
            status_code=404,
            detail="Notification not found"
        )

    notification.is_read = True
    db.commit()
    db.refresh(notification)

    return {
        "message": "Notification marked as read",
        "notification": notification
    }


# Mark all notifications as read
@router.patch("/read-all")
def mark_all_notifications_read(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.is_read == False
    ).update(
        {"is_read": True},
        synchronize_session=False
    )

    db.commit()

    return {"message": "All notifications marked as read"}

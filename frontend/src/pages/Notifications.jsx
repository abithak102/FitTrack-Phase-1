
import { useEffect, useState } from "react";
import api from "../services/api";
import "./Notifications.css";

function Notifications() {
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const fetchNotifications = async () => {
    try {
      setError("");
      const response = await api.get("/notifications/");
      setNotifications(response.data);
    } catch (err) {
      setError(
        err.response?.data?.detail || "Failed to load notifications."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchNotifications();
  }, []);

  const markAsRead = async (id) => {
    try {
      await api.patch(`/notifications/${id}/read`);
      await fetchNotifications();
    } catch (err) {
      setError(
        err.response?.data?.detail || "Could not update notification."
      );
    }
  };

  const markAllAsRead = async () => {
    try {
      await api.patch("/notifications/read-all");
      await fetchNotifications();
    } catch (err) {
      setError(
        err.response?.data?.detail || "Could not update notifications."
      );
    }
  };

  const unreadCount = notifications.filter(
    (item) => !item.is_read
  ).length;

  return (
    <div className="notifications-page">
      <div className="notifications-header">
        <div>
          <h1>Notifications</h1>
          <p>
            Stay updated with your fitness activities and reminders.
          </p>
        </div>

        {unreadCount > 0 && (
          <button
            className="mark-all-btn"
            onClick={markAllAsRead}
          >
            Mark all as read
          </button>
        )}
      </div>

      <div className="notification-summary">
        <div className="notification-summary-icon">🔔</div>
        <div>
          <h3>{notifications.length}</h3>
          <p>Total Notifications</p>
        </div>

        <div className="notification-summary-icon">📩</div>
        <div>
          <h3>{unreadCount}</h3>
          <p>Unread Notifications</p>
        </div>
      </div>

      {error && <div className="notification-error">{error}</div>}

      {loading ? (
        <p className="notification-message">Loading notifications...</p>
      ) : notifications.length === 0 ? (
        <div className="empty-notifications">
          <span>🔔</span>
          <h2>No notifications yet</h2>
          <p>Your workout reminders and goal alerts will appear here.</p>
        </div>
      ) : (
        <div className="notification-list">
          {notifications.map((item) => (
            <div
              key={item.id}
              className={`notification-card ${
                item.is_read ? "read" : "unread"
              }`}
            >
              <div className="notification-icon">🔔</div>

              <div className="notification-content">
                <h3>{item.title}</h3>
                <p>{item.message}</p>

                <small>
                  {item.created_at
                    ? new Date(item.created_at).toLocaleString()
                    : "Date unavailable"}
                </small>
              </div>

              {!item.is_read && (
                <button
                  className="mark-read-btn"
                  onClick={() => markAsRead(item.id)}
                >
                  Mark as read
                </button>
              )}

              {item.is_read && (
                <span className="read-label">Read</span>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Notifications;


import { useEffect, useState } from "react";
import api from "../services/api";
import "./Goals.css";

function Goals() {
  const [goals, setGoals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [editingId, setEditingId] = useState(null);

  const [formData, setFormData] = useState({
    goal_title: "",
    description: "",
    target_value: "",
    current_value: "0",
    unit: "kg",
    start_date: new Date().toISOString().slice(0, 10),
    target_date: "",
  });

  const fetchGoals = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await api.get("/goals/");
      setGoals(response.data);
    } catch (err) {
      setError(
        err.response?.data?.detail || "Unable to load goals."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchGoals();
  }, []);

  const handleChange = (event) => {
    const { name, value } = event.target;

    setFormData((previous) => ({
      ...previous,
      [name]: value,
    }));
  };

  const resetForm = () => {
    setEditingId(null);

    setFormData({
      goal_title: "",
      description: "",
      target_value: "",
      current_value: "0",
      unit: "kg",
      start_date: new Date().toISOString().slice(0, 10),
      target_date: "",
    });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    setError("");
    setSuccess("");

    const target = Number(formData.target_value);
    const current = Number(formData.current_value);

    if (!Number.isFinite(target) || target <= 0) {
      setError("Target value must be greater than zero.");
      return;
    }

    if (!Number.isFinite(current) || current < 0 || current > target) {
      setError("Current value must be between zero and target value.");
      return;
    }

    if (formData.target_date < formData.start_date) {
      setError("Target date must be on or after start date.");
      return;
    }

    const payload = {
      ...formData,
      target_value: target,
      current_value: current,
    };

    try {
      if (editingId) {
        await api.put(`/goals/${editingId}`, payload);
        setSuccess("Goal updated successfully!");
      } else {
        await api.post("/goals/", payload);
        setSuccess("Goal created successfully!");
      }

      resetForm();
      await fetchGoals();
    } catch (err) {
      setError(
        err.response?.data?.detail || "Unable to save goal."
      );
    }
  };

  const handleEdit = (goal) => {
    setEditingId(goal.id);

    setFormData({
      goal_title: goal.goal_title,
      description: goal.description || "",
      target_value: String(goal.target_value),
      current_value: String(goal.current_value),
      unit: goal.unit,
      start_date: goal.start_date,
      target_date: goal.target_date,
    });

    setError("");
    setSuccess("");

    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  };

  const handleDelete = async (goalId) => {
    const confirmed = window.confirm(
      "Are you sure you want to delete this goal?"
    );

    if (!confirmed) return;

    try {
      setError("");
      setSuccess("");

      await api.delete(`/goals/${goalId}`);

      if (editingId === goalId) {
        resetForm();
      }

      setSuccess("Goal deleted successfully!");
      await fetchGoals();
    } catch (err) {
      setError(
        err.response?.data?.detail || "Unable to delete goal."
      );
    }
  };

  if (loading) {
    return (
      <div className="goals-loading">
        Loading your fitness goals...
      </div>
    );
  }

  return (
    <div className="goals-page">
      <div className="goals-header">
        <div>
          <h1>My Fitness Goals</h1>
          <p>Create goals and track your fitness achievements.</p>
        </div>

        <button onClick={fetchGoals} className="refresh-goals-btn">
          Refresh Goals
        </button>
      </div>

      {error && <div className="goals-error">{error}</div>}
      {success && <div className="goals-success">{success}</div>}

      <section className="goal-form-section">
        <h2>{editingId ? "Edit Goal" : "Create New Goal"}</h2>

        <form onSubmit={handleSubmit} className="goal-form">
          <div className="goal-form-grid">
            <div className="goal-field">
              <label>Goal Title</label>
              <input
                type="text"
                name="goal_title"
                value={formData.goal_title}
                onChange={handleChange}
                placeholder="Example: Lose Weight"
                minLength={2}
                maxLength={100}
                required
              />
            </div>

            <div className="goal-field">
              <label>Unit</label>
              <select
                name="unit"
                value={formData.unit}
                onChange={handleChange}
                required
              >
                <option value="kg">kg</option>
                <option value="workouts">workouts</option>
                <option value="calories">calories</option>
                <option value="minutes">minutes</option>
                <option value="steps">steps</option>
                <option value="km">km</option>
              </select>
            </div>

            <div className="goal-field">
              <label>Target Value</label>
              <input
                type="number"
                name="target_value"
                value={formData.target_value}
                onChange={handleChange}
                min="0.01"
                step="any"
                required
              />
            </div>

            <div className="goal-field">
              <label>Current Progress</label>
              <input
                type="number"
                name="current_value"
                value={formData.current_value}
                onChange={handleChange}
                min="0"
                step="any"
                required
              />
            </div>

            <div className="goal-field">
              <label>Start Date</label>
              <input
                type="date"
                name="start_date"
                value={formData.start_date}
                onChange={handleChange}
                required
              />
            </div>

            <div className="goal-field">
              <label>Target Date</label>
              <input
                type="date"
                name="target_date"
                value={formData.target_date}
                onChange={handleChange}
                required
              />
            </div>

            <div className="goal-field goal-description">
              <label>Description</label>
              <textarea
                name="description"
                value={formData.description}
                onChange={handleChange}
                placeholder="Describe your fitness goal..."
                maxLength={500}
                rows={3}
              />
            </div>
          </div>

          <div className="goal-form-actions">
            <button type="submit" className="save-goal-btn">
              {editingId ? "Update Goal" : "Create Goal"}
            </button>

            {editingId && (
              <button
                type="button"
                className="cancel-goal-btn"
                onClick={resetForm}
              >
                Cancel
              </button>
            )}
          </div>
        </form>
      </section>

      <section className="goal-list-section">
        <div className="goal-list-heading">
          <h2>Your Goals</h2>
          <span>{goals.length} Goals</span>
        </div>

        {goals.length === 0 ? (
          <div className="no-goals">
            <h3>No Goals Yet</h3>
            <p>Create your first fitness goal to get started!</p>
          </div>
        ) : (
          <div className="goals-grid">
            {goals.map((goal) => {
              const percentage = Math.min(
                100,
                (goal.current_value / goal.target_value) * 100
              );

              return (
                <div className="goal-card" key={goal.id}>
                  <div className="goal-card-top">
                    <div>
                      <h3>{goal.goal_title}</h3>
                      <p>{goal.description || "No description provided."}</p>
                    </div>

                    <span
                      className={`goal-status ${
                        goal.status === "COMPLETED"
                          ? "completed"
                          : "active"
                      }`}
                    >
                      {goal.status}
                    </span>
                  </div>

                  <div className="goal-values">
                    <div>
                      <span>Current Progress</span>
                      <strong>
                        {goal.current_value} / {goal.target_value} {goal.unit}
                      </strong>
                    </div>

                    <strong>{percentage.toFixed(1)}%</strong>
                  </div>

                  <div className="goal-progress-track">
                    <div
                      className="goal-progress-fill"
                      style={{ width: `${percentage}%` }}
                    />
                  </div>

                  <div className="goal-dates">
                    <span>Start: {goal.start_date}</span>
                    <span>Target: {goal.target_date}</span>
                  </div>

                  <div className="goal-card-actions">
                    <button
                      className="edit-goal-btn"
                      onClick={() => handleEdit(goal)}
                    >
                      Edit / Update Progress
                    </button>

                    <button
                      className="delete-goal-btn"
                      onClick={() => handleDelete(goal.id)}
                    >
                      Delete
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </section>
    </div>
  );
}

export default Goals;

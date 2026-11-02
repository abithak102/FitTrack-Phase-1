
import { useEffect, useState } from "react";
import api from "../services/api";
import "./Workouts.css";

function Workouts() {
  const [workouts, setWorkouts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [editingId, setEditingId] = useState(null);

  const [formData, setFormData] = useState({
    workout_name: "",
    category: "Cardio",
    duration: "",
    calories_burned: "",
    workout_date: new Date().toISOString().split("T")[0],
  });

  // Load workouts
  const fetchWorkouts = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await api.get("/workouts/");
      setWorkouts(response.data);
    } catch (err) {
      setError(
        err.response?.data?.detail || "Unable to load workouts."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchWorkouts();
  }, []);

  // Handle input changes
  const handleChange = (event) => {
    const { name, value } = event.target;

    setFormData((previous) => ({
      ...previous,
      [name]: value,
    }));
  };

  // Reset form
  const resetForm = () => {
    setFormData({
      workout_name: "",
      category: "Cardio",
      duration: "",
      calories_burned: "",
      workout_date: new Date().toISOString().split("T")[0],
    });

    setEditingId(null);
  };

  // Add or Update workout
  const handleSubmit = async (event) => {
    event.preventDefault();

    setError("");
    setSuccess("");

    const workoutData = {
      ...formData,
      duration: Number(formData.duration),
      calories_burned: Number(formData.calories_burned),
    };

    try {
      if (editingId !== null) {
        await api.put(`/workouts/${editingId}`, workoutData);
        setSuccess("Workout updated successfully!");
      } else {
        await api.post("/workouts/", workoutData);
        setSuccess("Workout added successfully!");
      }

      resetForm();
      await fetchWorkouts();
    } catch (err) {
      setError(
        err.response?.data?.detail || "Unable to save workout."
      );
    }
  };

  // Edit workout
  const handleEdit = (workout) => {
    setEditingId(workout.id);

    setFormData({
      workout_name: workout.workout_name,
      category: workout.category,
      duration: String(workout.duration),
      calories_burned: String(workout.calories_burned),
      workout_date: workout.workout_date,
    });

    setError("");
    setSuccess("");

    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  };

  // Delete workout
  const handleDelete = async (workoutId) => {
    const confirmed = window.confirm(
      "Are you sure you want to delete this workout?"
    );

    if (!confirmed) {
      return;
    }

    setError("");
    setSuccess("");

    try {
      await api.delete(`/workouts/${workoutId}`);

      setSuccess("Workout deleted successfully!");

      if (editingId === workoutId) {
        resetForm();
      }

      await fetchWorkouts();
    } catch (err) {
      setError(
        err.response?.data?.detail || "Unable to delete workout."
      );
    }
  };

  return (
    <div className="workouts-page">
      <h1>Workout Management</h1>
      <p>Track and manage your daily fitness activities.</p>

      {/* ADD / EDIT FORM */}
      <section className="workout-form-section">
        <h2>
          {editingId !== null ? "Edit Workout" : "Add New Workout"}
        </h2>

        <form onSubmit={handleSubmit}>
          <label>Workout Name</label>
          <input
            type="text"
            name="workout_name"
            value={formData.workout_name}
            onChange={handleChange}
            placeholder="Example: Morning Running"
            minLength={2}
            maxLength={100}
            required
          />

          <label>Category</label>
          <select
            name="category"
            value={formData.category}
            onChange={handleChange}
          >
            <option value="Cardio">Cardio</option>
            <option value="Strength">Strength</option>
            <option value="Yoga">Yoga</option>
          </select>

          <label>Duration (minutes)</label>
          <input
            type="number"
            name="duration"
            value={formData.duration}
            onChange={handleChange}
            min="1"
            max="1440"
            required
          />

          <label>Calories Burned</label>
          <input
            type="number"
            name="calories_burned"
            value={formData.calories_burned}
            onChange={handleChange}
            min="0"
            max="10000"
            step="0.1"
            required
          />

          <label>Workout Date</label>
          <input
            type="date"
            name="workout_date"
            value={formData.workout_date}
            onChange={handleChange}
            required
          />

          <button type="submit">
            {editingId !== null ? "Update Workout" : "Add Workout"}
          </button>

          {editingId !== null && (
            <button
              type="button"
              className="cancel-btn"
              onClick={resetForm}
            >
              Cancel Edit
            </button>
          )}
        </form>

        {success && <p className="success-message">{success}</p>}
        {error && <p className="error-message">{error}</p>}
      </section>

      {/* WORKOUT LIST */}
      <section className="workout-list-section">
        <h2>My Workouts</h2>

        {loading ? (
          <p>Loading workouts...</p>
        ) : workouts.length === 0 ? (
          <p>No workouts found. Add your first workout!</p>
        ) : (
          <div className="workout-list">
            {workouts.map((workout) => (
              <div className="workout-card" key={workout.id}>
                <h3>{workout.workout_name}</h3>

                <p>Category: {workout.category}</p>
                <p>Duration: {workout.duration} minutes</p>
                <p>Calories: {workout.calories_burned} kcal</p>
                <p>Date: {workout.workout_date}</p>

                <div className="workout-actions">
                  <button
                    type="button"
                    className="edit-btn"
                    onClick={() => handleEdit(workout)}
                  >
                    Edit
                  </button>

                  <button
                    type="button"
                    className="delete-btn"
                    onClick={() => handleDelete(workout.id)}
                  >
                    Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}

export default Workouts;

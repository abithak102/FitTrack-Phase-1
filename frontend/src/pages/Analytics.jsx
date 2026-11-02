
import { useEffect, useState } from "react";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  PieChart,
  Pie,
  Cell,
  Legend
} from "recharts";

import api from "../services/api";
import "./Analytics.css";

const COLORS = ["#16a34a", "#2563eb", "#f59e0b", "#9333ea"];

function Analytics() {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const fetchAnalytics = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await api.get("/analytics/overview");
      setAnalytics(response.data);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        "Unable to load analytics information."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAnalytics();
  }, []);

  if (loading) {
    return (
      <div className="analytics-loading">
        Loading fitness analytics...
      </div>
    );
  }

  if (error) {
    return (
      <div className="analytics-page">
        <h1>Fitness Analytics</h1>
        <p className="analytics-error">{error}</p>
        <button onClick={fetchAnalytics}>Try Again</button>
      </div>
    );
  }

  const categoryData = analytics.category_breakdown || [];
  const monthlyData = analytics.monthly_statistics || [];

  return (
    <div className="analytics-page">

      <div className="analytics-header">
        <div>
          <h1>Fitness Analytics</h1>
          <p>Understand your fitness performance and activity.</p>
        </div>

        <button onClick={fetchAnalytics}>
          Refresh Analytics
        </button>
      </div>

      {/* SUMMARY CARDS */}
      <div className="analytics-stats">

        <div className="analytics-card">
          <span>🏋️</span>
          <h3>Total Workouts</h3>
          <h2>{analytics.total_workouts}</h2>
          <p>Completed workouts</p>
        </div>

        <div className="analytics-card">
          <span>🔥</span>
          <h3>Calories Burned</h3>
          <h2>
            {Number(analytics.total_calories).toLocaleString()}
          </h2>
          <p>Total calories</p>
        </div>

        <div className="analytics-card">
          <span>⏱️</span>
          <h3>Workout Duration</h3>
          <h2>{analytics.total_duration}</h2>
          <p>Total minutes</p>
        </div>

      </div>

      {/* CHARTS */}
      <div className="analytics-charts">

        <section className="analytics-chart-card">
          <h2>Monthly Workout Statistics</h2>

          {monthlyData.length === 0 ? (
            <p>No monthly workout data available yet.</p>
          ) : (
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={monthlyData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar
                  dataKey="workouts"
                  name="Workouts"
                  fill="#16a34a"
                />
                <Bar
                  dataKey="calories"
                  name="Calories"
                  fill="#f59e0b"
                />
              </BarChart>
            </ResponsiveContainer>
          )}
        </section>

        <section className="analytics-chart-card">
          <h2>Workout Category Analysis</h2>

          {categoryData.length === 0 ? (
            <p>No category data available yet.</p>
          ) : (
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={categoryData}
                  dataKey="count"
                  nameKey="category"
                  cx="50%"
                  cy="50%"
                  outerRadius={100}
                  label
                >
                  {categoryData.map((item, index) => (
                    <Cell
                      key={item.category}
                      fill={COLORS[index % COLORS.length]}
                    />
                  ))}
                </Pie>

                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          )}
        </section>

      </div>

    </div>
  );
}

export default Analytics;

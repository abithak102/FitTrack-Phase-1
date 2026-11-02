
import { useEffect, useState } from "react";
import api from "../services/api";
import "./Profile.css";

function Profile() {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const [profileForm, setProfileForm] = useState({
    username: "",
    email: "",
  });

  const [passwordForm, setPasswordForm] = useState({
    current_password: "",
    new_password: "",
  });

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      const response = await api.get("/auth/me");
      setProfile(response.data);
      setProfileForm({
        username: response.data.username,
        email: response.data.email,
      });
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to load profile.");
    } finally {
      setLoading(false);
    }
  };

  const handleProfileChange = (e) => {
    setProfileForm({
      ...profileForm,
      [e.target.name]: e.target.value,
    });
  };

  const handleProfileSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    try {
      const response = await api.patch("/auth/me", profileForm);
      setProfile(response.data);
      setProfileForm({
        username: response.data.username,
        email: response.data.email,
      });
      setSuccess("Profile updated successfully.");
    } catch (err) {
      setError(err.response?.data?.detail || "Profile update failed.");
    }
  };

  const handlePasswordChange = (e) => {
    setPasswordForm({
      ...passwordForm,
      [e.target.name]: e.target.value,
    });
  };

  const handlePasswordSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    try {
      const response = await api.patch(
        "/auth/change-password",
        passwordForm
      );

      setSuccess(response.data.message);
      setPasswordForm({
        current_password: "",
        new_password: "",
      });
    } catch (err) {
      setError(err.response?.data?.detail || "Password change failed.");
    }
  };

  if (loading) {
    return <div className="profile-page">Loading profile...</div>;
  }

  if (!profile) {
    return <div className="profile-page">{error || "Profile not found."}</div>;
  }

  return (
    <div className="profile-page">
      <div className="profile-header">
        <h1>My Profile</h1>
        <p>View and manage your FitTrack account.</p>
      </div>

      {error && <div className="profile-message error">{error}</div>}
      {success && <div className="profile-message success">{success}</div>}

      <div className="profile-card">
        <div className="profile-avatar">
          {profile.username.charAt(0).toUpperCase()}
        </div>

        <h2>{profile.username}</h2>
        <p>{profile.email}</p>
        <span>FitTrack Member</span>
      </div>

      <div className="profile-form-card">
        <h2>Edit Profile</h2>

        <form onSubmit={handleProfileSubmit}>
          <label>Username</label>
          <input
            type="text"
            name="username"
            minLength="3"
            maxLength="50"
            value={profileForm.username}
            onChange={handleProfileChange}
            required
          />

          <label>Email</label>
          <input
            type="email"
            name="email"
            value={profileForm.email}
            onChange={handleProfileChange}
            required
          />

          <button type="submit">Save Profile</button>
        </form>
      </div>

      <div className="profile-form-card">
        <h2>Change Password</h2>

        <form onSubmit={handlePasswordSubmit}>
          <label>Current Password</label>
          <input
            type="password"
            name="current_password"
            value={passwordForm.current_password}
            onChange={handlePasswordChange}
            minLength="8"
            maxLength="72"
            required
          />

          <label>New Password</label>
          <input
            type="password"
            name="new_password"
            value={passwordForm.new_password}
            onChange={handlePasswordChange}
            minLength="8"
            maxLength="72"
            required
          />

          <button type="submit">Change Password</button>
        </form>
      </div>
    </div>
  );
}

export default Profile;

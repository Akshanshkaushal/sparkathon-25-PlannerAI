import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

export const triggerEvent = async (data) => {
  try {
    const response = await axios.post(`${API_URL}/trigger-event`, data);
    return response.data;
  } catch (error) {
    console.error('Error triggering event:', error);
    throw error;
  }
};

export const updateUserPreferences = async (data) => {
  try {
    const response = await axios.post(`${API_URL}/user-preferences`, data);
    return response.data;
  } catch (error) {
    console.error('Error updating user preferences:', error);
    throw error;
  }
};
// src/components/dashboard/UserForm.jsx

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { triggerEvent, updateUserPreferences } from '../../api/eventApi';
import { Input } from "../ui/input";
import {Button} from '../ui/button';
import Loader from '../common/Loader';
import { LoaderFive, LoaderFour } from '../ui/loader';

const UserForm = () => {
  const [formData, setFormData] = useState({
    username: '',
    eventname: '',
    preferences: '',
    minBudget: '',
    maxBudget: '',
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(null);

    const summary = `${formData.eventname}_${formData.username}`;
    const data = {
      summary,
      preferences: formData.preferences.split(',').map(p => p.trim()),
      budget: {
        min: parseInt(formData.minBudget, 10),
        max: parseInt(formData.maxBudget, 10),
          },
    };

    try {
      const result = await triggerEvent(data);
      navigate('/my-cart', { state: { cartData: result } });
    } catch (err) {
      setError('Failed to fetch event data. Please try again.');
    } finally {
      setLoading(false);
       }
  };

  const handlePreferencesSubmit = async (e) => {
     e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(null);

    const summary = `${formData.eventname}_${formData.username}`;
    const data = {
      summary,
      preferences: formData.preferences.split(',').map(p => p.trim()),
      budget: {
        min: parseInt(formData.minBudget, 10),
        max: parseInt(formData.maxBudget, 10),
      },
    };
    try {
      await updateUserPreferences(data);
      setSuccess('Preferences and budget updated successfully!');
    } catch (err) {
      setError('Failed to update preferences. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  

  return (
    <form onSubmit={handleSubmit} className="w-full flex flex-col gap-4">
      <div className="grid  grid-cols-1 sm:grid-cols-2 gap-4">
        <Input
          label="Username (Email)"
          labelClassName="text-blue-600"
          name="username"
          value={formData.username}
          onChange={handleChange}
          placeholder="username@example.com"
          required
        />
        <Input
          label="Event Name"
          name="eventname"
          value={formData.eventname}
          onChange={handleChange}
          placeholder="Birthday, Wedding, etc."
          required
        />
      </div>

      <Input
        label="Preferences (comma-separated)"
        name="preferences"
        value={formData.preferences}
        onChange={handleChange}
        placeholder="books, gadgets, travel, cooking"
        required
      />

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <Input
          label="Minimum Budget ($)"
          name="minBudget"
          type="number"
          value={formData.minBudget}
          onChange={handleChange}
          placeholder="100"
          required
        />
        <Input
          label="Maximum Budget ($)"
          name="maxBudget"
          type="number"
          value={formData.maxBudget}
          onChange={handleChange}
          placeholder="500"
          required
        />
      </div>

      {error && (
        <div className="bg-red-100 border border-red-300 text-red-800 px-4 py-2 rounded-xl flex items-center gap-2 text-sm shadow">
          <svg className="w-5 h-5 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          {error}
        </div>
      )}

      {success && (
        <div className="bg-green-100 border border-green-300 text-green-800 px-4 py-2 rounded-xl flex items-center gap-2 text-sm shadow">
          <svg className="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
          </svg>
          {success}
        </div>
      )}

      <div className="flex flex-col sm:flex-row gap-2 mt-2">
        {loading ? (
          <div className="fixed inset-0 z-[100] flex items-center justify-center bg-slate-100 bg-opacity-90">
            <LoaderFive />
          </div>
        ) : (
          <div className='flex items-center  gap-11'>
            <Button type="submit" className="w-full mb-3">
              <svg className="w-6 h-6 mr-3 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
              Generate Event Plan
            </Button>
            <Button type="button" onClick={handlePreferencesSubmit} className="w-full mt-1">
              <svg className="w-6 h-6 mr-3 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
              Save Preferences Only
            </Button>
          </div>
        )}
      </div>

      <div className="text-center pt-3">
        <div className="inline-flex items-center gap-2 text-sm text-gray-700 bg-indigo-100/60 px-4 py-2 rounded-full shadow">
          <span className="text-xl">✨</span>
          <p>Our AI will analyze your preferences and create a personalized shopping plan</p>
        </div>
      </div>
    </form>
  );
};

export default UserForm;

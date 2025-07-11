import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { triggerEvent } from '../../api/eventApi';
import Input from '../common/Input';
import Button from '../common/Button';
import Loader from '../common/Loader';

const UserForm = () => {
  const [formData, setFormData] = useState({
    summary: '',
    preferences: '',
    minBudget: '',
    maxBudget: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const data = {
      summary: formData.summary,
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

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <Input label="Email Summary" name="summary" value={formData.summary} onChange={handleChange} placeholder="event_username@example.com" />
      <Input label="Preferences (comma-separated)" name="preferences" value={formData.preferences} onChange={handleChange} placeholder="books, gadgets, travel" />
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Input label="Min Budget" name="minBudget" type="number" value={formData.minBudget} onChange={handleChange} placeholder="100" />
        <Input label="Max Budget" name="maxBudget" type="number" value={formData.maxBudget} onChange={handleChange} placeholder="500" />
      </div>
      {loading ? <Loader /> : <Button type="submit" className="w-full">Generate Event Plan</Button>}
      {error && <p className="text-red-500 text-center">{error}</p>}
    </form>
  );
};

export default UserForm;
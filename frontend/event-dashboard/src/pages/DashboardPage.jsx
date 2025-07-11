import React from 'react';
import UserForm from '../components/dashboard/UserForm';
import Card from '../components/common/Card';

const DashboardPage = () => {
  return (
    <div>
      <h1 className="text-3xl font-bold text-text-primary mb-6">Create Your Event</h1>
      <Card>
        <UserForm />
      </Card>
    </div>
  );
};

export default DashboardPage;
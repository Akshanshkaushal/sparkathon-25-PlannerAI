# Event Planner AI

Event Planner AI is a full-stack web application that leverages AI to automate event planning and smart shopping. Users can create personalized event plans, manage budgets, and receive intelligent product and gift recommendations, all through a modern, responsive dashboard.

## Features

- **AI-Powered Event Planning:** Generate event plans tailored to user preferences, event type, and budget.
- **Smart Shopping Cart:** View, manage, and track recommended products and gifts for your event.
- **Budget Management:** Set and monitor spending limits for different event categories (e.g., cake, decorations, gifts).
- **Personalized Recommendations:** Receive curated suggestions for gifts and event items based on your interests.
- **Calendar Integration:** Connect your calendar to sync and manage event schedules (UI ready for integration).
- **Modern UI:** Built with React, Tailwind CSS, and shadcn/ui for a seamless user experience.

## Tech Stack

- **Frontend:** React, Tailwind CSS, shadcn/ui, Vite
- **Backend:** Python Flask (REST API)
- **Other:** Calendar integration (planned), modular component architecture

## Getting Started

### Prerequisites
- Node.js (v16+ recommended)
- Python 3.8+

### Setup

#### 1. Clone the repository
```bash
git clone https://github.com/Akshanshkaushal/sparkathon-25-PlannerAI.git
cd sparkathon-25-PlannerAI
```

#### 2. Frontend Setup
```bash
cd frontend/event-dashboard
npm install
npm run dev
```
The frontend will be available at `http://localhost:5173` by default.

#### 3. Backend Setup
```bash
cd ../../backend
python -m venv venv
venv\Scripts\activate  # On Windows
# Or: source venv/bin/activate  # On Mac/Linux
pip install -r requirements.txt
python run.py
```
The backend will be available at `http://localhost:5000` by default.

## Folder Structure

```
backend/
  app/
    agents/
    api/
    services/
frontend/
  event-dashboard/
    src/
      components/
      pages/
      api/
```

## Usage
1. Fill out the event form with your preferences and budget.
2. Generate an event plan to receive AI-powered recommendations.
3. Review your cart, event details, and budget breakdown.
4. (Optional) Connect your calendar for event scheduling.

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License
This project is licensed under the MIT License.

---

**Event Planner AI** — Smart Shopping & Planning for Every Occasion

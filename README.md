# AI Student Career Recommendation

An AI-powered platform that analyzes student data and generates personalized career and success recommendations, built with a Python backend and a TypeScript frontend.

## Features

- Student data-driven career recommendation engine
- REST API backend (FastAPI)
- MongoDB-backed data storage
- TypeScript frontend for user interaction
- Seed script for populating sample/test data

## Tech Stack

**Backend:** Python, FastAPI, MongoDB
**Frontend:** TypeScript, CSS
**Other:** `build.sh` for deployment, `requirements.txt` for Python dependencies

## Project Structure

```
├── backend/              # API and recommendation logic
├── frontend/             # TypeScript frontend app
├── run.py                # Application entry point
├── seed.py               # Seeds sample data into the database
├── test_recommend.py     # Tests for recommendation logic
├── requirements.txt      # Python dependencies
├── build.sh              # Build script
├── .env.example           # Example environment variables (copy to .env)
└── package-lock.json     # Frontend dependency lock file
```

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/vedant18dhonde-design/AI-for-Student-career-recommendation.git
cd AI-for-Student-career-recommendation
```

### 2. Backend setup

```bash
python -m venv venv
venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in your own values (MongoDB URI, secret keys, etc.):

```bash
copy .env.example .env
```

Seed the database (optional, for sample data):

```bash
python seed.py
```

Run the backend:

```bash
python run.py
```

### 3. Frontend setup

```bash
cd frontend
npm install
npm run dev
```

## Testing

```bash
python test_recommend.py
```

## Environment Variables

See `.env.example` for required variables. Never commit your actual `.env` file — it's excluded via `.gitignore`.

## License

Not yet specified.

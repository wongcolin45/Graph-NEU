# NEU Roadmaps

An interactive web application that helps Northeastern students visualize their course roadmap to graduation. Explore course prerequisites, track progress, and see branching paths for potential majors or minors.

## Tech Stack

- **Frontend:** Next.js 15, React 19, React Flow, MUI
- **Backend:** FastAPI (Python)
- **Database:** PostgreSQL (populated via web scraping)

## Hosting

| Component | Service |
|-----------|---------|
| Frontend | Vercel |
| Backend | Render |
| Database | Supabase / Neon |

## Features

- Visual course graphs using **React Flow**
- Track completed courses with real-time updates
- Fetch course data from a **PostgreSQL** database populated through web scraping
- View dependencies and future options for any course
- Intelligent backend logic via **FastAPI**

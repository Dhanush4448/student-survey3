\# Student Survey (SWE-645 – HW3)



\- \*\*Frontend:\*\* React + Vite (`frontend/`)

\- \*\*Backend:\*\* FastAPI + SQLModel (`backend/`)

\- \*\*K8s manifests:\*\* `k8s/`

\- \*\*CI/CD:\*\* Jenkinsfile builds \& deploys to Kubernetes



\## Local Dev

\- Backend: `cd backend \&\& python -m uvicorn app.main:app --host 0.0.0.0 --port 8080`

\- Frontend: `cd frontend \&\& npm run dev` (set `VITE\_API\_BASE=http://localhost:8080` in `.env`)



\## Deploy (CI/CD)

\- Jenkins pipeline points at this repo

\- Docker Hub user: `dhanush853`




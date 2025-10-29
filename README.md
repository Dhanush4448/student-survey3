\# Student Survey (SWE-645 – HW3)



Full-stack CRUD app for the Student Survey assignment.



\- Frontend: React + Vite (frontend/)

\- Backend: FastAPI + SQLModel (backend/)

\- Kubernetes: manifests in k8s/

\- CI/CD: Jenkins Pipeline builds Docker images and deploys to K8s

\- Docker Hub user: dhanush853



------------------------------------------------------------

Repo layout

------------------------------------------------------------

student-survey3/

├─ backend/

│  ├─ app/

│  │  ├─ main.py          # FastAPI app + routes

│  │  ├─ models.py        # SQLModel table(s)

│  │  ├─ schemas.py       # Pydantic models

│  │  └─ crud.py          # DB helpers

│  └─ requirements.txt

├─ frontend/

│  ├─ src/App.jsx         # React form + table

│  ├─ src/api.js          # API\_BASE from env/runtime

│  └─ Dockerfile

├─ k8s/                   # Namespace, Deployments, Services, HPAs, ConfigMap, Secret template

├─ Jenkinsfile            # Windows agent-friendly pipeline

└─ README.md



------------------------------------------------------------

Local development

(run backend and frontend in two separate terminals)

------------------------------------------------------------



1\) Backend (FastAPI)

------------------------------------------------------------

cd backend

python -m venv .venv

.\\.venv\\Scripts\\Activate.ps1

pip install -r requirements.txt

\# if EmailStr complains:

\# pip install email-validator==2.2.0



\# run on 8080

python -m uvicorn app.main:app --host 0.0.0.0 --port 8080



\# health check

Invoke-RestMethod http://127.0.0.1:8080/healthz



\# example POST

$body = @{

&nbsp; first\_name="Ada"; last\_name="Lovelace"; street\_address="1 Code Rd"; city="Arlington"; state="VA";

&nbsp; zip="22202"; telephone="555-1234"; email="ada@example.com"; date\_of\_survey="2066-02-28";

&nbsp; liked\_most="students"; how\_interested="friends"; recommend\_likelihood="Very Likely"

} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8080/surveys -Body $body -ContentType "application/json"



2\) Frontend (Vite)

------------------------------------------------------------

cd frontend

\# point UI to backend

echo VITE\_API\_BASE=http://localhost:8080 > .env



npm install

npm run dev

\# Vite prints the URL, e.g. http://localhost:5175/



------------------------------------------------------------

API summary

------------------------------------------------------------

GET    /healthz                 -> {"status":"ok"}

GET    /surveys                 -> list all surveys

POST   /surveys                 -> create survey (SurveyCreate body)

GET    /surveys/{id}

PUT    /surveys/{id}

DELETE /surveys/{id}



------------------------------------------------------------

Docker (optional local images)

------------------------------------------------------------

\# from repo root

docker build -t studentsurvey-frontend:dev .\\frontend

docker build -t studentsurvey-backend:dev  .\\backend



------------------------------------------------------------

Kubernetes (manifests)

------------------------------------------------------------

Assumptions:

\- Namespace: studentsurvey

\- Frontend talks to http://studentsurvey-backend:8080 (ClusterIP)

\- If you don’t have RDS yet, skip applying k8s/secret-db.yaml (backend uses SQLite)



\# base objects

kubectl apply -f k8s/namespace.yaml

kubectl -n studentsurvey apply -f k8s/configmap-frontend.yaml

kubectl -n studentsurvey apply -f k8s/backend-service.yaml

kubectl -n studentsurvey apply -f k8s/frontend-service.yaml

\# optional HPAs

kubectl -n studentsurvey apply -f k8s/hpa-backend.yaml

kubectl -n studentsurvey apply -f k8s/hpa-frontend.yaml



Deployments are templated for CI to inject image/tag.

For manual tests, edit image names in:

\- k8s/backend-deployment.yaml

\- k8s/frontend-deployment.yaml



Then:

kubectl -n studentsurvey apply -f k8s/backend-deployment.yaml

kubectl -n studentsurvey apply -f k8s/frontend-deployment.yaml

kubectl -n studentsurvey get svc,deploy,pods



------------------------------------------------------------

CI/CD (Jenkins)

------------------------------------------------------------

\- Create a Pipeline job (or Multibranch) pointing to this repo

\- Add Jenkins credentials id: dockerhub-creds (Docker Hub username/password)

\- Ensure Jenkins agent has Docker and kubectl



Jenkinsfile variables:

&nbsp; FRONTEND\_IMG = docker.io/dhanush853/studentsurvey-frontend

&nbsp; BACKEND\_IMG  = docker.io/dhanush853/studentsurvey-backend

&nbsp; IMAGE\_TAG    = ${BUILD\_NUMBER}



Stages:

&nbsp; 1) Checkout

&nbsp; 2) Build (docker build)

&nbsp; 3) Push (docker push)

&nbsp; 4) K8s base (namespace, services, configmap, hpa)

&nbsp; 5) Deploy (apply deployments with ${IMAGE\_TAG})

&nbsp; 6) Show endpoints (kubectl get svc,deploy,pods)



------------------------------------------------------------

Troubleshooting

------------------------------------------------------------

EmailStr error (email-validator not installed):

&nbsp; pip install email-validator==2.2.0



Port 8080 already in use (Windows):

&nbsp; netstat -ano | findstr :8080

&nbsp; tasklist /FI "PID eq <PID>"

&nbsp; taskkill /PID <PID> /F



Frontend “Submit failed. Check backend/API\_BASE.”:

&nbsp; - Ensure backend is running on 8080

&nbsp; - Confirm frontend/.env contains:

&nbsp;     VITE\_API\_BASE=http://localhost:8080

&nbsp; - Restart `npm run dev` after changing .env



CORS errors in local dev:

&nbsp; - Backend allows http://localhost:\* by default



------------------------------------------------------------

License

------------------------------------------------------------

For class use (SWE-645 HW3).




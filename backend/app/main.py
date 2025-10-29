from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session
from .models import Survey
from .schemas import SurveyCreate
from .database import init_db, get_session

# Short description (required per assignment): FastAPI REST API providing CRUD for Student Survey

app = FastAPI(title="Student Survey API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.post("/surveys", response_model=dict)
def create(payload: SurveyCreate, session: Session = Depends(get_session)):
    survey = Survey(**payload.dict())
    from .crud import create_survey
    survey = create_survey(session, survey)
    return {"id": survey.id}

@app.get("/surveys", response_model=list[dict])
def list_all(session: Session = Depends(get_session)):
    from .crud import list_surveys
    surveys = list_surveys(session)
    return [s.dict() for s in surveys]

@app.get("/surveys/{survey_id}", response_model=dict)
def get_one(survey_id: int, session: Session = Depends(get_session)):
    from .crud import get_survey
    s = get_survey(session, survey_id)
    if not s:
        raise HTTPException(404, "Not found")
    return s.dict()

@app.put("/surveys/{survey_id}", response_model=dict)
def update_one(survey_id: int, payload: SurveyCreate, session: Session = Depends(get_session)):
    from .crud import update_survey
    updated = update_survey(session, survey_id, payload.dict())
    if not updated:
        raise HTTPException(404, "Not found")
    return updated.dict()

@app.delete("/surveys/{survey_id}", response_model=dict)
def delete_one(survey_id: int, session: Session = Depends(get_session)):
    from .crud import delete_survey
    ok = delete_survey(session, survey_id)
    if not ok:
        raise HTTPException(404, "Not found")
    return {"deleted": True}

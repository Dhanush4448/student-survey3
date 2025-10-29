from sqlmodel import select
from .models import Survey

def create_survey(session, data: Survey):
    session.add(data)
    session.commit()
    session.refresh(data)
    return data

def list_surveys(session):
    return session.exec(select(Survey)).all()

def get_survey(session, survey_id: int):
    return session.get(Survey, survey_id)

def update_survey(session, survey_id: int, payload: dict):
    survey = session.get(Survey, survey_id)
    if not survey: return None
    for k, v in payload.items():
        setattr(survey, k, v)
    session.add(survey)
    session.commit()
    session.refresh(survey)
    return survey

def delete_survey(session, survey_id: int) -> bool:
    survey = session.get(Survey, survey_id)
    if not survey: return False
    session.delete(survey)
    session.commit()
    return True

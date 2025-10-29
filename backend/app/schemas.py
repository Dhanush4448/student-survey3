from pydantic import BaseModel, EmailStr
from datetime import date

class SurveyCreate(BaseModel):
    first_name: str
    last_name: str
    street_address: str
    city: str
    state: str
    zip: str
    telephone: str
    email: EmailStr
    date_of_survey: date
    liked_most: str
    how_interested: str
    recommend_likelihood: str

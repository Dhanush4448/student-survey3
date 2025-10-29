﻿from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date

class Survey(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    street_address: str
    city: str
    state: str
    zip: str
    telephone: str
    email: str
    date_of_survey: date
    liked_most: str
    how_interested: str
    recommend_likelihood: str

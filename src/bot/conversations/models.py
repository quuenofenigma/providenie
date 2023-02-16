from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr, confloat, conint, constr


class FormBase(BaseModel):
    """Базовая модель для анкет."""

    name: str
    birthday: date
    city: Optional[str]
    email: Optional[EmailStr]
    phone_number: constr(min_length=11, max_length=15)

    class Config:
        min_anystr_length = 1


class VolunteerForm(FormBase):
    """Модель для анкеты на волонтерство."""

    city: str
    message: str
    email: EmailStr

    class Config:
        min_anystr_length = 1


class ChatForm(FormBase):
    """Модель для анкеты на вступление в чат."""

    child_name: str
    current_chat: str
    how_find_fund: str
    place_of_birth: str
    child_diagnosis: str
    date_aplication: date
    surgery_on_child: str
    child_height: conint(ge=30, le=45)
    child_weight: confloat(ge=1, le=2.5)
    child_term_of_birth: conint(ge=22, le=37)


class FundForm(ChatForm):
    """Модель для анкеты на отправку заявки в фонд."""

    city: str
    address: str
    programm: str
    email: EmailStr
    another_fund_help: str
    another_fund_member: str
    family_members: conint(ge=2)

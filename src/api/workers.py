from datetime import date
from http import HTTPStatus

from fastapi import APIRouter, File, Form, UploadFile
from src.controller.workers import WorkersController
from src.models import WorkerWithProfessionOut
from starlette.requests import Request

router = APIRouter()


@router.post('/', status_code=HTTPStatus.CREATED.value)
async def add_worker(
    req: Request,
    last_name: str = Form(...),
    first_name: str = Form(...),
    patronymic: str = Form(''),
    birthday: date = Form(...),
    profession: str = Form(...),
    identification: UploadFile = File(...),
    drivers_license: UploadFile = File(None),
    order_of_acceptance_to_work: UploadFile = File(None),
    training_information: UploadFile = File(None),
    speciality_course_information: UploadFile = File(None),
    another_drive_license: UploadFile = File(None),
    medical_certificate: UploadFile = File(None),
    certificate_of_competency: UploadFile = File(None),
    instructed_information: UploadFile = File(None),
    emergency_driving_certificate: UploadFile = File(None),
) -> WorkerWithProfessionOut:
    return await WorkersController.add(
        req,
        last_name,
        first_name,
        patronymic,
        birthday,
        profession,
        identification=identification,
        driving_license=drivers_license,
        order_of_acceptance_to_work=order_of_acceptance_to_work,
        training_information=training_information,
        speciality_course_information=speciality_course_information,
        another_drive_license=another_drive_license,
        medical_certificate=medical_certificate,
        certificate_of_competency=certificate_of_competency,
        instructed_information=instructed_information,
        emergency_driving_certificate=emergency_driving_certificate,
    )

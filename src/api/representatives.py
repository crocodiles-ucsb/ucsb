from datetime import datetime

from fastapi import APIRouter, File, Form, UploadFile

router = APIRouter()


@router.post('/workers')
async def add_worker(
    last_name: str = Form(...),
    first_name: str = Form(...),
    birthday: datetime = Form(...),
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
):
    pass

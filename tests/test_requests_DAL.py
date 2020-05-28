from datetime import date

import pytest
from src.api.catalogs import CatalogType
from src.DAL.catalogs_dal import CatalogsDAL
from src.DAL.contractors_dal import ContractorsDAL
from src.DAL.documents_dal import DocumentsDAL
from src.DAL.registration import UniqueLinkRegistrationParams
from src.DAL.representatives_dal import RepresentativesDAL
from src.DAL.requests import RequestsDAL
from src.DAL.users.contractor_representative import (
    ContractorRepresentativeAddingParams,
    ContractorRepresentatives,
)
from src.database.database import create_session
from src.database.models import (
    Request,
    RequestStatus,
    Worker,
    WorkerInRequest,
    WorkerInRequestStatus,
)
from src.exceptions import DALError
from src.models import OutUser, RequestIn


@pytest.fixture()
async def _add_object_of_work():
    return await CatalogsDAL.add_item(
        CatalogType.objects_of_work,
        'object_of_work',
        value=None,
        out_model=CatalogType.objects_of_work.out_model,
    )


@pytest.fixture()
def _add_contractor(contractor):
    pass


@pytest.fixture()
def request_in():
    return RequestIn(object_of_work_id=1, contract_id=3)


@pytest.fixture()
def representative_adding_params():
    return ContractorRepresentativeAddingParams(
        last_name='last_name',
        first_name='first_name',
        patronymic='patronymic',
        telephone_number='telephone_number',
        email='email',
        contractor_id=1,
    )


@pytest.fixture()
def contractor_representative_out():
    return OutUser(id=1, type='contractor_representative', username='123')


@pytest.fixture()
async def _add_contract(upload_file):
    await DocumentsDAL.add_contract(1, 'title', upload_file)


@pytest.fixture()
async def _add_contractor_representative(
    representative_adding_params, contractor_representative_out
):
    res = await RepresentativesDAL.add(representative_adding_params)
    await ContractorRepresentatives().register_user(
        UniqueLinkRegistrationParams(
            contractor_representative_out.username, 'password', res.uuid
        )
    )


@pytest.mark.asyncio
@pytest.mark.usefixtures(
    '_add_object_of_work',
    '_add_contractor',
    '_add_contract',
    '_add_contractor_representative',
)
async def test_add_request(request_in, contractor_representative_out):
    res = await RequestsDAL.add(contractor_representative_out, request_in)
    with create_session() as session:
        request = session.query(Request).filter(Request.id == 1).one()
        assert request.contractor_id == res.contractor_id == 1
        assert request.object_of_work_id == res.object_of_work_id == 1
        assert request.contract_id == res.contract_id == 3
        assert request.status == RequestStatus.WAITING_FOR_READINESS


@pytest.fixture()
async def _add_request(request_in, contractor_representative_out):
    await RequestsDAL.add(contractor_representative_out, request_in)


@pytest.mark.asyncio
@pytest.mark.usefixtures(
    '_add_object_of_work',
    '_add_contractor',
    '_add_contract',
    '_add_contractor_representative',
    '_add_request',
)
async def test_add_same_request_second_time_will_delete_first(
    request_in, contractor_representative_out
):
    res = await RequestsDAL.add(contractor_representative_out, request_in)
    assert res.id == 2
    assert res.contract_id == 3
    assert res.contractor_id == 1
    with create_session() as session:
        assert not session.query(Request).filter(Request.id == 1).first()
        assert session.query(Request).filter(Request.id == 2).one()


@pytest.fixture()
async def _add_worker(
    _add_profession, worker_fields, contractor_representative_out, profession
):
    await RepresentativesDAL.add_worker(
        **worker_fields,
        profession=profession,
        contractor_representative=contractor_representative_out
    )


@pytest.mark.asyncio
@pytest.mark.usefixtures(
    '_add_object_of_work',
    '_add_contractor',
    '_add_contract',
    '_add_contractor_representative',
    '_add_request',
    '_add_worker',
)
async def test_add_same_request_second_time_will_delete_first_and_delete_workers_in_request_connected_with_request(
    request_in, contractor_representative_out
):
    await RequestsDAL.add_worker_to_request(contractor_representative_out, 1, 1)
    await RequestsDAL.add(contractor_representative_out, request_in)
    with create_session() as session:
        assert not session.query(Request).filter(Request.id == 1).first()
        request = session.query(Request).filter(Request.id == 2).one()
        assert len(request.workers_in_request) == 0


@pytest.mark.asyncio
@pytest.mark.usefixtures(
    '_add_object_of_work',
    '_add_contractor',
    '_add_contract',
    '_add_contractor_representative',
    '_add_request',
    '_add_worker',
)
async def test_add_worker_to_request(contractor_representative_out):
    res = await RequestsDAL.add_worker_to_request(contractor_representative_out, 1, 1)
    with create_session() as session:
        worker_in_request: WorkerInRequest = session.query(WorkerInRequest).filter(
            WorkerInRequest.id == 1
        ).one()
        worker = session.query(Worker).filter(Worker.id == 1).one()
        assert len(worker.worker_requests) == 1
        assert worker_in_request.request_id == 1
        assert worker_in_request.status == WorkerInRequestStatus.WAITING_FOR_READINESS


@pytest.mark.asyncio
@pytest.mark.usefixtures(
    '_add_object_of_work',
    '_add_contractor',
    '_add_contract',
    '_add_contractor_representative',
    '_add_worker',
)
async def test_add_worker_to_request_if_request_does_not_exists(
    contractor_representative_out,
):
    with pytest.raises(DALError):
        await RequestsDAL.add_worker_to_request(contractor_representative_out, 1, 1)


@pytest.mark.asyncio
@pytest.mark.usefixtures(
    '_add_object_of_work',
    '_add_contractor',
    '_add_contract',
    '_add_contractor_representative',
    '_add_request',
    '_add_worker',
)
async def test_add_worker_to_request_if_worker_already_in_request(
    contractor_representative_out,
):
    await RequestsDAL.add_worker_to_request(contractor_representative_out, 1, 1)
    with pytest.raises(DALError):
        await RequestsDAL.add_worker_to_request(contractor_representative_out, 1, 1)


@pytest.mark.asyncio
@pytest.mark.usefixtures(
    '_add_object_of_work',
    '_add_contractor',
    '_add_contract',
    '_add_contractor_representative',
    '_add_profession',
    '_add_request',
)
async def test_add_worker_to_request_if_worker_does_not_belongs_to_contractor(
    contractor_representative_out, representative_adding_params, upload_file, profession
):
    res = await ContractorsDAL.add(
        'another_title',
        'another_address',
        'another_ogrn',
        'another_inn',
        inn_document=upload_file,
        ogrn_document=upload_file,
    )
    representative_adding_params.contractor_id = res.id
    representative_to_adding = await RepresentativesDAL.add(
        representative_adding_params
    )
    representative = await ContractorRepresentatives().register_user(
        UniqueLinkRegistrationParams(
            username='another_representative',
            password='123',
            uuid=representative_to_adding.uuid,
        )
    )
    worker = await RepresentativesDAL.add_worker(
        representative,
        '1',
        '1',
        date.today(),
        profession=profession,
        identification=upload_file,
    )
    with pytest.raises(DALError):
        await RequestsDAL.add_worker_to_request(
            contractor_representative_out, request_id=1, worker_id=worker.id
        )


@pytest.mark.asyncio
@pytest.mark.usefixtures(
    '_add_object_of_work',
    '_add_contractor',
    '_add_contract',
    '_add_contractor_representative',
    '_add_request',
    '_add_worker',
)
async def test_delete_worker_from_request(contractor_representative_out):
    await RequestsDAL.add_worker_to_request(contractor_representative_out, 1, 1)
    await RequestsDAL.delete_worker_from_request(
        contractor_representative_out, request_id=1, worker_id=1
    )
    with create_session() as session:
        assert (
            not session.query(WorkerInRequest).filter(WorkerInRequest.id == 1).first()
        )


@pytest.mark.asyncio
@pytest.mark.usefixtures(
    '_add_object_of_work',
    '_add_contractor',
    '_add_contract',
    '_add_contractor_representative',
    '_add_request',
)
async def test_delete_worker_from_request_if_worker_does_not_exists(
    contractor_representative_out,
):
    with pytest.raises(DALError):
        await RequestsDAL.delete_worker_from_request(
            contractor_representative_out, request_id=1, worker_id=1
        )


@pytest.mark.asyncio
@pytest.mark.usefixtures(
    '_add_object_of_work',
    '_add_contractor',
    '_add_contract',
    '_add_contractor_representative',
)
async def test_delete_worker_from_request_if_request_doe_not_exists(
    contractor_representative_out,
):
    with pytest.raises(DALError):
        await RequestsDAL.delete_worker_from_request(
            contractor_representative_out, request_id=1, worker_id=1
        )

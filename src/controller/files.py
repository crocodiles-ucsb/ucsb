from src.DAL.documents_dal import DocumentsDAL
from starlette.responses import FileResponse


class FilesController:
    @staticmethod
    async def get_file(file_id: str) -> FileResponse:
        return await DocumentsDAL.get(file_id)

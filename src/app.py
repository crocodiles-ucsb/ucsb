from src.app_creation import create_app
from src.database.database import Base

Base.metadata.create_all()
app = create_app()

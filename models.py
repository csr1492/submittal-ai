from sqlalchemy import Column, String, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type = Column(String)
    filename = Column(String)
    extracted_text = Column(Text)
    structured_data = Column(JSON)

from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel as Document
from pydantic import Field, validator  # noqa

from app.commons.fields import ObjectIdStr  # noqa


class EmbeddedDocument(Document):
    ...


class TrackableDocumentMixin(Document):
    created_by: str = Field(...)
    created_at: datetime = Field(...)
    updated_by: str = Field(...)
    updated_at: datetime = Field(...)


class ExternalReference(EmbeddedDocument):
    id: Optional[str] = Field(
        None, title="Identificador único no sistema de origem"
    )
    source: str = Field(..., title="Sistema de origem")
    metadata: Dict[str, Any] = Field(
        None, title="Metadados do sistema de origem"
    )

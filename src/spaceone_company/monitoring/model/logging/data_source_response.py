from schematics import Model
from schematics.types.compound import PolyModelType
from src.spaceone_company.monitoring.model.logging import log_model


class DataSourceMetadata(Model):
    _metadata = PolyModelType(log_model, serialized_name='metadata', serialize_when_none=False)
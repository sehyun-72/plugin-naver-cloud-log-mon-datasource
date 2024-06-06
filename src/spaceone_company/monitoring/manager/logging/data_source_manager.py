import logging
from spaceone.core.manager import BaseManager
from src.spaceone_company.monitoring.connector.log_connector import LogConnector
from src.spaceone_company.monitoring.model.logging.data_source_response import DataSourceMetadata
from src.spaceone_company.monitoring.manager.metadata_manager import MetadataManager

_LOGGER = logging.getLogger(__name__)


class Log_Manager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def init(params):
        options = params['options']
        meta_manager = MetadataManager()
        response_model = DataSourceMetadata({'_metadata': meta_manager.get_data_source_metadata()}, strict=False)
        return response_model.to_primitive()

    def verify(self, params):
        log_connector: LogConnector = self.locator.get_connector('Log', **params)
        log_connector.set_connect(params.get('scheme'), params.get('options'), params.get('secret_data'))
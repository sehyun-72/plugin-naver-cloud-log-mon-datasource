import logging
from spaceone.core.manager import BaseManager
from src.spaceone_company.monitoring.model.logging.metadata.metadata import LogMetadata
from src.spaceone_company.monitoring.model.logging.metadata.metadata_dynamic_field import TextDyField, DateTimeDyField, ListDyField, \
    MoreField
from src.spaceone_company.monitoring.conf.monitoring_conf import *

_LOGGER = logging.getLogger(__name__)

class MetadataManager(BaseManager):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def get_data_source_metadata():
        metadata = LogMetadata.set_fields(
            name='activitylog-table',
            fields=[
                MoreField.data_source('Operation Name', options={
                    'layout': {
                        'name': 'Log Details',
                        'type': 'popup',
                        'options': {
                            'layout': {
                                'type': 'raw'
                            }
                        }
                    }
                }),
                TextDyField.data_source('Status', 'status.localized_value'),
                TextDyField.data_source('Caller', 'caller'),
                DateTimeDyField.data_source('Event Time', 'event_timestamp'),
            ]
        )
        return metadata
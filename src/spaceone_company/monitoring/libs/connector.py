from __future__ import print_function
import ncloud_vpc
import ncloud_monitoring
import logging
import boto3
from keystoneauth1 import session
from keystoneauth1.identity import v3
import swiftclient
from spaceone.core.connector import BaseConnector

__all__ = ['NaverCloudConnector']

_LOGGER = logging.getLogger(__name__)
DEFAULT_SCHEMA = 'naver_client_secret'


class NaverCloudConnector(BaseConnector):

    def __init__(self, *args: object, **kwargs: object):
        """
        kwargs
            - schema
            - options
            - secret_data

        secret_data = {
            'ncloud_access_key_id': AKI,
            'ncloud_secret_key': SK,
            'domain_id': 'DI',
            'project_id': 'PI',
            'db_kind_code': 'DKC',
            'cdn_instance_no': 'CIN',
            'instance_no': 'IN',
            'bucket_name': 'BN'
        }
        """

        super().__init__(*args, **kwargs)
        self.client = None
        self.vpc_client = None
        self.set_connect(kwargs['secret_data'])
        # self.set_connect_storage(kwargs['secret_data'])

    def set_connect(self, secret_data: object) -> object:
        configuration_vpc = ncloud_vpc.Configuration()
        configuration_vpc.access_key = secret_data['ncloud_access_key_id']
        configuration_vpc.secret_key = secret_data['ncloud_secret_key']
        self.vpc_client = ncloud_vpc.V2Api(ncloud_vpc.ApiClient(configuration_vpc))

    def set_connect_storage(self, secret_data: object):
        object_endpoint_url = 'https://kr.object.ncloudstorage.com'
        object_storage_access_key = secret_data['ncloud_access_key_id']
        object_storage_secret_key = secret_data['ncloud_secret_key']
        self.object_storage_client = boto3.client(service_name='s3',
                                                  endpoint_url=object_endpoint_url,
                                                  aws_access_key_id=object_storage_access_key,
                                                  aws_secret_access_key=object_storage_secret_key
                                                  )

        archive_endpoint_url = 'https://kr.archive.ncloudstorage.com:5000/v3'
        archive_storage_access_key = secret_data['ncloud_access_key_id']
        archive_storage_secret_key = secret_data['ncloud_secret_key']
        domain_id = secret_data['domain_id']
        project_id = secret_data['project_id']
        auth = v3.Password(auth_url=archive_endpoint_url,
                           username=archive_storage_access_key,
                           password=archive_storage_secret_key,
                           project_id=project_id,
                           user_domain_id=domain_id)
        auth_session = session.Session(auth=auth)
        self.archive_storage_client = swiftclient.Connection(retries=5, session=auth_session)

    def verify(self, **kwargs):
        if self.server_client is None:
            self.set_connect(kwargs['secret_data'])
            return "ACTIVE"

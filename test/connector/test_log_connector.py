import os
import json
import unittest
from spaceone.core.unittest.runner import RichTestRunner

# 테스트할 클래스 import
from src.spaceone_company.monitoring.connector.logging.log_connector import LogConnector

# def _get_credentials():
#     with open(GOOGLE_APPLICATION_CREDENTIALS_PATH) as json_file:
#         json_data = json.load(json_file)
#         return json_data
class TestLog(unittest.TestCase):

    def setUp(self):
        # 테스트 시작 전 설정
        self.connector = LogConnector(
            secret_data= {
                ''
            },
            page_data={'page_num': 1, 'page_size': 10},
            api_key={'api_key': 'your_api_key'}
        )

    def test_init(self):
        # init 테스트
        v_info = self.connector.init({'options': {}})
        # 결과 검증

    def test_verify(self):
        # verify 테스트
        schema = ''
        options = {}
        result = self.connector.verify({'schema': schema, 'options': options})
        # 결과 검증

    def test_log_list(self):
        # log_list 테스트
        params = {
            'query': {
                'resource_id': '',
                'name': 'projects/bluese-cloudone-20200113',
                'filters': [
                    {
                        'resource_type': 'gce_instance',
                        'labels': [
                            {
                                'key': 'resource.labels.instance_id',
                                'value': ''
                            }
                        ]
                    }
                ]
            },
            'start': '2023-03-21T00:00:00Z',
            'end': '2023-03-21T23:00:00Z'
        }

        resource_stream = self.connector.list_server_group()
        # 결과 검증


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)

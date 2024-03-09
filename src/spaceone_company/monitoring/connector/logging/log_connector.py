from spaceone.core import utils
from src.spaceone_company.monitoring.libs.connector import NaverCloudConnector
import logging
import requests
import time
import hashlib
import hmac
import base64
from spaceone.core.connector import BaseConnector

_LOGGER = logging.getLogger("cloudforet")
class LogConnector(BaseConnector):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.access_key = kwargs['secret_data'].get('ncloud_access_key_id')
        self.secret_key = kwargs['secret_data'].get('ncloud_secret_key')
        self.page_num = kwargs['page_data'].get('page_num')
        self.page_size = kwargs['page_data'].get('page_size')
        self.api_key = kwargs['api_key'].get('api_key')
        self.base_url = "https://cloudloganalytics.apigw.ntruss.com/api/{regionCode}-v1/"
    def make_signature(self, method, uri):
        timestamp = str(int(time.time() * 1000))
        message = f"{method} {uri}\n{timestamp}\n{self.access_key}"
        signature = base64.b64encode(hmac.new(self.secret_key.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).digest()).decode('utf-8')
        return signature, timestamp

    def call_api(self, method, uri, payload=None):
        signature, timestamp = self.make_signature(method, uri)
        headers = {
            "x-ncp-apigw-timestamp": timestamp,
            "x-ncp-iam-access-key": self.access_key,
            "x-ncp-apigw-signature-v2": signature,
            "x-ncp-apigw-api-key": self.api_key,
            "content-type": "application/json"
        }

        full_url = self.base_url + uri
        if method.upper() == 'GET':
            response = requests.get(full_url, headers=headers, json=payload)
        else:
            response = requests.get(full_url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            _LOGGER.error(f"API call failed with status code {response.status_code}: {response.text}")
            return None

#####
    def list_server_group(self):
        log_filters = self.get('filters', [])
        server_group_list = []

        # 기본 URI
        base_uri = "https://cloudloganalytics.apigw.ntruss.com/api/{regionCode}-v1/classic/servers"

        for log_filter in log_filters:
            # 필터별로 URI 생성
            uri = base_uri + f"?{log_filter}"

            payload = {
                "pageNo": self.page_num,
                "pageSize": self.page_size
            }
            method = "GET"
            try:
                response = self.call_api(method, uri, payload)
                if 'result' in response:
                    for group in response['result']:
                        server_group_list.append(group)
            except Exception as e:
                _LOGGER.error(f"Exception when calling Cloud Insight API: {e}")

        return server_group_list

    def log_count(self):
        log_count_list = []
        payload = {

        }
        method = "GET"
        uri = "https://cloudloganalytics.apigw.ntruss.com/api/{regionCode}-v1/logs/count/total"
        try:
            response = self.call_api(method, uri, payload)  # 수정된 call_api 메소드 호출 시 페이로드 전달
            for group in response['result']:
                log_count_list.append(group)
        except Exception as e:
            _LOGGER.error(f"Exception when calling Cloud Insight API: {e}")

        return log_count_list

    def list_bucket(self):
        bucket_list = []
        payload = {
            "pageNo": self.page_no,
            "pageSize": self.page_size,
        }
        method = "GET"
        uri = "https://cloudloganalytics.apigw.ntruss.com/api/{regionCode}-v1/export/bucketsl"
        try:
            response = self.call_api(method, uri, payload)  # 수정된 call_api 메소드 호출 시 페이로드 전달
            for group in response['result']:
                bucket_list.append(group)
        except Exception as e:
            _LOGGER.error(f"Exception when calling Cloud Insight API: {e}")

        return bucket_list

    def get_usage(self):
        usage_list = []
        payload = {
            "pageNo": self.page_no,
            "pageSize": self.page_size,
        }
        method = "GET"
        uri = "https://cloudloganalytics.apigw.ntruss.com/api/{regionCode}-v1/capacity"
        try:
            response = self.call_api(method, uri, payload)  # 수정된 call_api 메소드 호출 시 페이로드 전달
            for group in response['']:
                usage_list.append(group)
        except Exception as e:
            _LOGGER.error(f"Exception when calling Cloud Insight API: {e}")

        return usage_list


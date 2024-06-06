import sys
import os
import hashlib
import hmac, json
import base64, time, requests


class LogConnector:
    def __init__(self, secret_data):
        self.base_url = 'https://cloudloganalytics.apigw.ntruss.com'
        self.secret_data = secret_data

    def make_signature(self, access_key, secret_key, method, uri, timestamp):
        message = method + " " + uri + "\n" + timestamp + "\n" + access_key
        message = bytes(message, 'UTF-8')
        secret_key = bytes(secret_key, 'UTF-8')
        signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
        return signingKey

    def send_request(self, endpoint):
        url = f"{self.base_url}{endpoint}"
        method = 'GET'
        timestamp = str(int(time.time() * 1000))
        access_key = self.secret_data['ncloud_access_key_id']
        secret_key = self.secret_data['ncloud_secret_key']

        headers = {
            'x-ncp-apigw-signature-v2': self.make_signature(access_key, secret_key, method, endpoint, timestamp),
            'x-ncp-apigw-timestamp': timestamp,
            'x-ncp-iam-access-key': access_key,
            'Content-Type': 'application/json'
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            servers = response.json()
            print(json.dumps(servers, indent=4))
        else:
            print(f"Error: {response.status_code}, {response.text}")

        return response

    def get_Classic_server_list(self, region_code, page_no, page_size):
        return self.send_request(endpoint= f"/api/{region_code}-v1/vpc/servers?pageNo={page_no}&pageSize={page_size}")
    def get_CDB_Mysql_list(self, region_code, page_no, page_size):
        return self.send_request(endpoint=f"/api/{region_code}-v1/classic/servers/mysql?pageNo={page_no}&pageSize={page_size}")
    def get_CDB_Mssql_list(self, region_code, page_no, page_size):
        return self.send_request(endpoint=f"/api/{region_code}-v1/classic/servers/mssql?pageNo={page_no}&pageSize={page_size}")
    def get_Baremetal_server_list(self, region_code, page_no, page_size):
        return self.send_request(endpoint=f"/api/{region_code}-v1/classic/servers/baremetal?pageNo={page_no}&pageSize={page_size}")
    def get_vpc_list(self, region_code, page_no, page_size):
        return self.send_request(endpoint=f"/api/{region_code}-v1/vpc/servers?pageNo={page_no}&pageSize={page_size}")
    def get_vpc_CDB_Mysql_list(self, region_code, page_no, page_size):
        return self.send_request(endpoint=f"/api/{region_code}-v1/vpc/servers?pageNo={page_no}&pageSize={page_size}")
    def get_vpc_CDB_MSSQL_list(self, region_code, page_no, page_size):
        return self.send_request(endpoint=f"/api/{region_code}-v1/vpc/servers?pageNo={page_no}&pageSize={page_size}")
    def get_vpc_CDB_MongoDB_list(self, region_code, page_no, page_size):
        return self.send_request(endpoint=f"/api/{region_code}-v1/vpc/servers?pageNo={page_no}&pageSize={page_size}")
    def get_vpc_CDB_PostgreSQL_list(self, region_code, page_no, page_size):
        return self.send_request(endpoint=f"/api/{region_code}-v1/vpc/servers?pageNo={page_no}&pageSize={page_size}")
    def get_vpc_Baremetal_list(self, region_code, page_no, page_size):
        return self.send_request(endpoint=f"/api/{region_code}-v1/vpc/servers?pageNo={page_no}&pageSize={page_size}")
    def get_vpc_SES_list(self, region_code, page_no, page_size):
        return self.send_request(endpoint=f"/api/{region_code}-v1/vpc/servers?pageNo={page_no}&pageSize={page_size}")
    def get_vpc_cloud_data_list(self, region_code, page_no, page_size):
        return self.send_request(endpoint=f"/api/{region_code}-v1/vpc/servers?pageNo={page_no}&pageSize={page_size}")
    def get_vpc_ncloud_kubernetes_list(self, region_code, page_no, page_size):
        return self.send_request(endpoint=f"/api/{region_code}-v1/vpc/servers?pageNo={page_no}&pageSize={page_size}")

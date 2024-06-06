import logging
from spaceone.core.manager import BaseManager
from src.spaceone_company.monitoring.connector.logging.log_connector import LogConnector
from src.spaceone_company.monitoring.model.logging import Log, ActivityLogInfo

_LOGGER = logging.getLogger(__name__)


class MonitoringManager(BaseManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def list_logs(self, params):
        results = []

        # LogConnector 인스턴스 생성
        log_connector = LogConnector(params.get('secret_data'))

        # # 필터 설정
        # filters = self.set_filter(params)
        # _LOGGER.debug(f'[list_logs] filter: {filters}')

        # 로그 가져오기
        logs = log_connector.get_vpc_CDB_Mysql_list(
            region_code=params.get('region_code'),
            page_no=params.get('page_no', 1),
            page_size=params.get('page_size', 10)
        )

        # 로그 필터링 및 변환
        for log in logs.get('items', []):
            if filter_log := self.keyword_filter(log, params):
                results.append(ActivityLogInfo(filter_log, strict=False))

        return Log({'results': results})

    @staticmethod
    def keyword_filter(log, params):
        if keyword := params.get('keyword'):
            value = log.get('event_name', '')  # 적절한 event_name 키값 사용
            if value and keyword.lower() in value.lower():
                return log
        else:
            return log

    @staticmethod
    def set_filter(params):
        filters = f"eventTimestamp ge '{params['start']}' and eventTimestamp le '{params['end']}'"

        query = params.get('query', {})
        if 'resource_uri' in query:
            filters = f"{filters} and resourceURI eq '{query['resource_uri']}'"

        return filters
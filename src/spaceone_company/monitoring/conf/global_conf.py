CONNECTORS = {
    'NaverCloudConnector': {
            'backend': 'spaceone.inventory.libs.connector.NaverCloudConnector',
        },
    'LogConnector':{
        'backend': 'spaceone_company.monitoring.connector.logging.LogConnector'

    }
}
LOG = {
    'filters':{
        'masking':{
            'rules':{
                'Log.list':[
                    'secret_data'
                ]
            }
        }
    }
}

HANDLERS = {
}

ENDPOINTS = {
}

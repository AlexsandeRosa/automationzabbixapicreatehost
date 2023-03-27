from zabbix_api import ZabbixAPI

zapi = ZabbixAPI('http://127.0.0.1/zabbix')
zapi.login('Admin', 'zabbix')

zapi.proxy.update({
        "proxyid": "10580",
        "hosts": [
            {
                "hostid": "10578"
            },
        ]
        })
# Autor: Alexsander Rosa
# Data: 25/03/2023
# Versão: 1.0

# Importa biblioteca zabbix_api
from zabbix_api import ZabbixAPI

# Variáveis de URL de acesso, nome de usuário e senha
URL = 'http://127.0.0.1/zabbix'
USERNAME = 'Admin'
PASSWORD = 'zabbix'

# Cria variável chamada zapi que chama a API do zabbix e fornece os parametros para login
zapi = ZabbixAPI(server=URL, timeout=180, validate_certs=False)
# Realiza o Login na API
zapi.login(USERNAME, PASSWORD)

# Cria uma variável chamada hosts e chama a variável zapi com suas funções para coletar informa>hosts = zapi.proxy.get({
"output": ['proxyid', 'host'],
})

# Mostra na tela os dados encontrados
for host in hosts:
    print(host)

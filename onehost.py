# Autor: Alexsander Rosa
# Data: 25/03/2023
# Versão: 1.0

# Importa biblioteca zabbix_api
from zabbix_api import ZabbixAPI

# Variáveis de URL de acesso, nome de usuário e senha
zapi = ZabbixAPI('http://127.0.0.1/zabbix')
zapi.login('Admin', 'zabbix')

# Chama a variável com o parâmetro para adicionar o host.
zapi.host.create({
            "host": "Router1", # Nome do Host
            "status": 0,       # Status do Host 0 marca como habilitado
            "interfaces": [{   # Configuração de interface SNMPv2
                "type": 2,
                "main": "1",
                "useip": 1,
                "ip": "100.100.100.2", # Endereço IP do Host
                "dns": "", 
                "port": "161", 
                "details": {
                    "version": "2", # Versão de SNMP
                    # "bulk": "0",
                    "community": "TESTE", # Community
                    "contextname": "",
                }
            }],
            "groups": [{"groupid": "20"}], # Definição do grupo pertecente desse host utilizando o ID coletado com o script anterior
            "templates": [{"templateid": "10186"}] # Definição do template para o host utilizando o ID coletado com o script anterior
        })

        # Exibe uma mensagem de confirmação
print("Host '{hostname}' adicionado com sucesso!")
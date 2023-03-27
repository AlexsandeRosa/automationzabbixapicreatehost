# Autor: Alexsander Rosa
# Data: 25/03/2023
# Versão: 1.0

# Realiza o import do csv e da API do Zabbix.
import csv 
from zabbix_api import ZabbixAPI

# Cria variáveis e atribuições para o login
zapi = ZabbixAPI('http://127.0.0.1/zabbix')
zapi.login('Admin', 'zabbix')

# Abre o nosso arquivo csv e define o delimitador.
with open('/tmp/hosts1.csv', 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    next(csv_reader)  # Pula a linha de cabeçalho
    
    # Loop para ler o arquivo linha a linha
    for row in csv_reader:
        hostname, ip = row
        print(f"IP: '{ip}'")

        # Cria o host no Zabbix
        host = zapi.host.create({
"host": hostname,
            "status": 0,
            "interfaces": [{
                "type": 2,
                "main": "1",
                "useip": 1,
                "ip": ip,
                "dns": "",
                "port": "161",
                "details": {
                    "version": "3", # Versão do SNMP
                    "securityname": "roost", # Security Name da comunicação
                    "securitylevel": 2, # Nível de segurança do SNMPv3 (2) indica authPriv 
                    "authpassphrase": "d41d8cd98f00b204e9800998ecf8427e",
                    "authprotocol": 3, # Protocolo de autenticação utilizado (3) indica SHA256
                    "privpassphrase": "d41d8cd98f00b204e9800998ecf8427e",
                    "privprotocol": 1, # Protocolo de priv utilizado (2) indica AES128;
                    "contextname": "",
                }
            }],
            "groups": [{"groupid": "20"}],
            "templates": [{"templateid": "10188"}]
        })
        # Exibe uma mensagem de confirmação
        print(f"Host '{hostname}' adicionado com sucesso!")
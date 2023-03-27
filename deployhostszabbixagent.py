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
                "type": 1, # Define tipo da interface para agent
                "main": "1",
                "useip": 1,
                "ip": ip,
                "dns": "",
                "port": "10050", # Define a porta do agent
                }
            }],
            "groups": [{"groupid": "20"}],
            "templates": [{"templateid": "10188"}]
        })
        # Exibe uma mensagem de confirmação
        print(f"Host '{hostname}' adicionado com sucesso!")
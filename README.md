# automationzabbixapicreatehost
Automatizando Criação de Hosts no Zabbix

### Introdução

- A automação em ambientes de tecnologia permite que as tarefas possam ser executadas com muito mais segurança, reduzindo as chances de erros. Dessa forma, ela traz agilidade no desenvolvimento e operações. Um dos fatores mais importantes na automação é a melhora no nível de qualidade. Com parâmetros estabelecidos, as entregas cumprirão exatamente a função esperada, evitando retrabalhos e perda de eficiência. Com mais segurança, agilidade e qualidade, as empresas conseguem reduzir custos. Além disso, os colaboradores deixam de executar tarefas mecânicas para se concentrarem em atividades que realmente possam agregar valor para a organização. Automação também é um item essencial para ambientes de monitoramento. Neste post veremos como automatizar a adição de hosts em um ambiente de monitoramento utilizando a ferramenta open source Zabbix.

### Informações de versionamento e observações

- Estes testes foram realizados utilizando as seguintes versões de sistema operacional e aplicação.
 
1. Zabbix 6.0.14 LTS
2. Zabbix API 0.5.5
3. Ubuntu Server 22.04 LTS

- Este post não aborda a configuração de SNMP ou Agent em dispositivos monitorados, são citadas apenas configurações do servidor de monitoramento.

## Pre Requisitos para a automação

1. Instalação do python3.

```bash
apt install python3 -y
```

1. Instalação do pip3.

```bash
apt install python3-pip
```

1. Instalação da biblioteca da API do Zabbix.

```bash
pip install zabbix_api
```
## Adicionando um único host para testar a API.

- Para realizar o teste da API, vamos adicionar um único host e verificar o comportamento para que então possamos criar o nosso arquivo *csv* que será usado para adicionar vários hosts de uma única vez. Mas, para isso precisamos realizar algumas tarefas primeiro como criar um grupo no Zabbix e escolher um template que vamos aplicar a este host para que possamos coletar os seus IDs e então seguir com o deploy do nosso host.

### Coletando ID do grupo

- Para esse exemplo criamos um grupo chamado “TESTE”, abaixo segue o script com os devidos comentários para coletar as informações que precisamos do grupo.
1. Vamos criar um arquivo com a extensão .py para que possamos escrever o script, crie-o com o seguinte comando:

```bash
nano getgroups.py
```

        2. Agora podemos seguir com a criação do script..

```python
# Autor: Alexsander Rosa
# Data: 25/03/2023
# Versão: 1.0

# Importa biblioteca zabbix_api
from zabbix_api import ZabbixAPI

# Variáveis de URL de acesso, nome de usuário e senha
URL ='http://127.0.0.1/zabbix'
USERNAME ='Admin'
PASSWORD = 'zabbix'

# Cria variável chamada zapi que chama a API do zabbix e fornece os parametros para login 
zapi = ZabbixAPI(server=URL, timeout=180, validate_certs=False)
# Realiza o Login na API
zapi.login(USERNAME, PASSWORD)

# Cria uma variável chamada hosts e chama a variável zapi com suas funções para coletar informações dos hosts
# Observe que estamos filtrando apenas ID e Nome para a informação ser mais objetiva
hosts = zapi.hostgroup.get({
    "output": ['groupid', 'name'],
})

# Mostra na tela os dados encontrados
for host in hosts:
    print (host)
```

- Dê permissão de execução para o script criado.

```python
chmod +x getgroups.py
```

- Utilize o seguinte comando para executar o script.

```python
python3 getgroups.py
```
- **Resultado:**
    - Observe que podemos ver as informações do grupo que criamos assim como o seu ID, isso vai ser muito importante para adicionarmos os hosts.

![image](https://user-images.githubusercontent.com/98989377/228008555-cf0c0c0e-8484-4826-a2f3-c2f8ab7250b9.png)

## Coletando ID do Template

1. Agora que sabemos o ID do grupo, vamos criar um script para que possamos escolher um template, e então coletar o seu ID. Neste exemplo vamos usar o template Roost Disponibilidade.

- Crie um arquivo com o seguinte comando.

```python
nano gettemplate.py
```

- Crie o script para coletar as informações dos templates.

```python
# Autor: Alexsander Rosa
# Data: 25/03/2023
# Versão: 1.0

# Importa biblioteca zabbix_api
from zabbix_api import ZabbixAPI

# Variáveis de URL de acesso, nome de usuário e senha
URL ='http://127.0.0.1/zabbix'
USERNAME ='Admin'
PASSWORD = 'zabbix'

# Cria variável chamada zapi que chama a API do zabbix e fornece os parametros para login 
zapi = ZabbixAPI(server=URL, timeout=180, validate_certs=False)
# Realiza o Login na API
zapi.login(USERNAME, PASSWORD)

# Cria uma variável chamada hosts e chama a variável zapi com suas funções para coletar informações dos hosts
# Observe que estamos filtrando apenas ID e Nome para a informação ser mais objetiva
hosts = zapi.template.get({
    "output": ['templateid', 'name'],
})

# Mostra na tela os dados encontrados
for host in hosts:
    print (host)
```

- De permissão de execução para o script criado.

```python
chmod +x gettemplate.py
```

- Execute o script.

```python
python3 gettemplate.py
```

- **Resultado**
    - Observe que podemos ver o template que criamos assim como o seu ID, isso vai ser muito importante para adicionarmos os hosts mais a frente.
    ![image](https://user-images.githubusercontent.com/98989377/228009400-588bf491-e07f-43fe-9692-8286a2f4c9f7.png)

1. Agora que temos o ID do grupo e o ID do template podemos adicionar o nosso host único para validar o funcionamento da API.
- Crie um arquivo com o seguinte comando.

```python
nano onehost.py
```

- Crie o script para adicionar o host.

```python
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
```

- De permissão de execução para o script.

```python
chmod +x onehost.py
```

- Utilize o seguinte comando para executar o script.

```python
python3 onehost.py
```
- **Resultado**
    - Observe que o host foi adicionado com sucesso no seu devido grupo utilizando o template desejado.
    ![image](https://user-images.githubusercontent.com/98989377/228009830-35dbd7c5-6c82-4890-81e3-f232163848b3.png)
    ![image](https://user-images.githubusercontent.com/98989377/228009934-e62f7f26-bc13-4272-9a6d-6366070c4725.png)
    
   ## Links de informações importantes da documentação do Zabbix  para criação de scripts de automação.

[https://www.zabbix.com/documentation/6.0/en/manual/api/reference/hostinterface/object](https://www.zabbix.com/documentation/6.0/en/manual/api/reference/hostinterface/object)

[https://www.zabbix.com/documentation/6.0/en/manual/api/reference/host/object#host](https://www.zabbix.com/documentation/6.0/en/manual/api/reference/host/object#host)

## Automação de criação de Hosts - SNMPv2

1. Agora que verificamos que a API do Zabbix está funcionando perfeitamente podemos automatizar a criação de hosts. Primeiro iremos criar um arquivo .csv para ser usado pelo script para listar os hosts a serem adicionados, utilize o excel para adicionar os hosts da seguinte forma. Neste exemplo estamos utilizando virgula “,” como delimitador, é importante que na primeira linha da nossa tabela seja usado o nome das variáveis que vamos utilizar no script.
![image](https://user-images.githubusercontent.com/98989377/228010622-0ca502c8-4c68-4f95-84d7-6d08d00ce716.png)
É de extrema importância salvar a planilha com as informações de hosts em formato .csv UTF-8, caso contrário o python não vai poder interpretar os caracteres o que vai fazer com que o nosso script não funcione.
![image](https://user-images.githubusercontent.com/98989377/228010720-2b9c9a81-63c8-4e31-919d-8c375fc230ac.png)
1. Faça o upload do arquivo criado com o hosts para dentro da pasta `/tmp` do Zabbix server para que possamos utilizar ela no script. Você pode utilizar o FileZilla ou qualquer aplicação de sua preferência para isso.
2. Agora que já temos o arquivo com os nossos dados criados podemos criar o arquivo para o nosso script:

```python
nano deployhosts.py
```

Dentro do arquivo vamos escrever o nosso script.

```python
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
            "host": hostname, # Utiliza a variável para configurar o nome do Host
            "status": 0, # Status do Host 0 define como habilitado
            "interfaces": [{
                "type": 2,
                "main": "1",
                "useip": 1,
                "ip": ip, # Utiliza a variável para configurar o IP do Host
                "dns": "",
                "port": "161", # Porta do SNMP
                "details": {
                    "version": "2", # Versão de SNMP
                    "community": "TESTE", # Community do SNMP
                    "contextname": "",
                }
            }],
            "groups": [{"groupid": "20"}], # Group ID
            "templates": [{"templateid": "10186"}] # Template ID
        })
        # Exibe uma mensagem de confirmação
        print(f"Host '{hostname}' adicionado com sucesso!")
```

1. De permissão de execução para o script e em seguida o execute.

```python
chmod +x deployhosts.py
python3 deployhosts.py
```
![image](https://user-images.githubusercontent.com/98989377/228011041-134f8004-cfe9-4c9c-ab24-54c82cf44766.png)
![image](https://user-images.githubusercontent.com/98989377/228011079-3dcb4bc7-a7d8-41d8-bc0d-49f44c903763.png)

## Automação de criação de Hosts - SNMPv3

- Visando a segurança do ambiente, é sempre recomendado e uma boa prática a utilização da versão 3 do SNMP.

Aqui está o exemplo de um script para configurar dispositivos utilizando SNMPv3 com as partes do código comentadas para o melhor entendimento. A lógica de criação do arquivo CSV é a mesma, o que vamos modificar é apenas a versão do SNMP e adicionar os parâmetros necessários para a autenticação.

```python
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
```

## Automação de criação de Hosts - Zabbix Agent

1. Para monitoramento de servidores que utilizam o Zabbix Agent basta alterarmos alguns parâmetros no nosso script.

```python
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
```

## Automação de criação de Hosts - Proxy

- Também é possível fazer a automação do vinculo entre hosts e proxies. Para isso precisamos executar algumas consultas na API do Zabbix para podermos encontrar os parâmetros para a criação do Script.
1. Coletar ID do proxy.

```python
# Autor: Alexsander Rosa
# Data: 25/03/2023
# Versão: 1.0

# Importa biblioteca zabbix_api
from zabbix_api import ZabbixAPI

# Variáveis de URL de acesso, nome de usuário e senha
URL ='http://127.0.0.1/zabbix'
USERNAME ='Admin'
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
    print (host)
```
![image](https://user-images.githubusercontent.com/98989377/228011782-ad2d0bbc-3eda-452e-a2f3-6c6d70753fba.png)

1. Coletar ID do host que será adicionado ao proxy .

```python
#Autor: Alexsander Rosa
# Data: 25/03/2023
# Versão: 1.0

# Importa biblioteca zabbix_api
from zabbix_api import ZabbixAPI

# Variáveis de URL de acesso, nome de usuário e senha
URL ='http://127.0.0.1/zabbix'
USERNAME ='Admin'
PASSWORD = 'zabbix'

# Cria variável chamada zapi que chama a API do zabbix e fornece os parametros para login 
zapi = ZabbixAPI(server=URL, timeout=180, validate_certs=False)
# Realiza o Login na API
zapi.login(USERNAME, PASSWORD)

# Cria uma variável chamada hosts e chama a variável zapi com suas funções para coletar informa># Observe que estamos filtrando apenas ID e Nome para a informação ser mais objetiva
hosts = zapi.host.get({
    "output": ['hostid', 'name'],
})

# Mostra na tela os dados encontrados
for host in hosts:
    print (host)
```
![image](https://user-images.githubusercontent.com/98989377/228011872-27841cac-a8ad-4008-9baa-487bc090f9a3.png)

1. Adicionando o host ao proxy.

```python
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
```

### Conclusão

- A cultura de inovação, produtividade e melhoria contínua estão presentes em toda empresa que busque diferencial competitivo no mercado e queira crescer e expandir os seus negócios. Com a utilização da API do Zabbix é possível tornar as nossas atividades mais escaláveis, competitivas e seguras.


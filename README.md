# Desafio onCase para Data Engineering
### Projeto que visa realizar um crawler de uma página de notícias. Foi usado a página [Aos Fatos](https://www.aosfatos.org)

Processo de deploy e preparação do ambiente numa máquina Linux com Ubuntu.
### Fazendo o deploy numa máquina Linux (distro Ubuntu) e a captura dos dados.
##### Dentro deste repositório temos o arquivo `deploy.sh` ele é responsável em fazer toda a preparação do ambiente na `/home` do usuário.

Ele será responsável em:
- Realizar algumas atualizações do sistema para instalação do Python 3.7;
- Mesmo o git já estando instalado, realizo a instalação durante o processo, a fim de garantir que usuário esteja apenas com o `deploy.sh`;
- Será necessário dar permissão de execução ao `deploy.sh` com o comando `chmod +x deploy.sh`
- Durante o processo, alguns passos de instalações pedirão para precionar `ENTER` para ou `S`.
- Realiza o `clone` do projeto;
- Cria a Virtual Environment do Python instalado durante o processo;
- Instala o framework do [Scrapy](https://scrapy.org/)

Durante a execução do `deploy.sh`ele também:
- Realiza o crawl;
- Salva um arquivo.json com o resultado do crawl;

# Problemas comuns
### Caso haja algum problema de instalação, reexecute o `deploy.sh`.



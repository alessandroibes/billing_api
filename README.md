# Billing API

## Descrição
API para processar arquivos CSV contendo informações de dívidas, gerando boletos e enviando e-mails.

O projeto possui um endpoint `/upload/`que recebe um arquivo `.csv` e gera boletos para cada linha do arquivo, enviando email a cada boleto gerado com sucesso. A cada boleto gerado, o sistema verifica se o mesmo já foi gerado anteriormente consultado uma estrutura mantida no Redis. A estrura no Redis apenas grava cada debId já processado associado ao hash gerado do arquivo, com isso, temos a lista de todos os boletos gerados para o arquivo. Por motivo de performance, o debId dos boletos gerados são mantidos em memória e salvos no Redis apenas ao final do processo.

## Como executar

### Requisitos
- Docker
- Docker Compose

### Passos para executar pelo Docker
1. Clone o repositório
2. Execute `docker-compose up --build` para iniciar o serviço
3. Acesse a API em `http://localhost:8000`

### Passos para executar a aplicação localmente
1. Clone o repositório
2. Entre na raiz do projeto executando `cd billing_api`
2. Crie um ambiente virtual
3. É preciso ter o Redis instalado ou executando no Docker.
    - O host e a porta devem estar definidos no arquivo: `/src/api/config.py`
4. Instale as dependências executando `pip install -r src/dependencies/requirements-dev.txt`
5. Entre na pasta **/src** executando `cd src`
6. Execute `uvicorn main:app --reload`
7. Acesse a API em `http://localhost:8000`

### Passos para rodar os testes
1. Clone o repositório
2. Crie um ambiente virtual
3. Instale as dependências executando `pip install -r src/dependencies/requirements-dev.txt`
3. Execute `pytest` do terminal

## Estrutura do Projeto
- `src/api/`: Contém todo o código da aplicação
    - `src/application_layer/`: Contém o código específico da camada de aplicação
        - `src/application_layer/adapters/`: Serviços
        - `src/application_layer/use_cases/`: Casos de Uso
    - `src/domain_layer`: Contém o código específico da camada de domínio
        - `src/domain_layer/models/`: Modelos de domínio
        - `src/domain_layer/ports/`: Classes abstratas que devem ser implementadas pelos serviços
    - `src/presentation_layer/`: Contém o código específico da camada de apresentação
        - `src/presentation_layer/views/`: Endpoints
- `src/dependencies`: Contém os arquivos utilizados para instalação das dependências do projeto
- `src/tests`: Contém os testes unitários e de integração da aplicação
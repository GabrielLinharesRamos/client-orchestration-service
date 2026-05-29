# Sistema Mundo Invest

# Visão Geral

O Sistema Mundo Invest é uma API backend desenvolvida em FastAPI responsável por:

- gerenciamento de clientes
- processamento de webhooks
- integração simulada com Pipefy via GraphQL
- controle de eventos processados com idempotência

A aplicação foi construída utilizando arquitetura em camadas, separando responsabilidades entre rotas, serviços, schemas, models e repositórios.

# Fluxo da Aplicação

#### estrutura do projeto:

![project_structure.svg](project_structure.svg)

- Client → consumidor da API responsável por enviar requisições HTTP para a aplicação.
- Routes → camada HTTP da aplicação responsável pelos endpoints, requests/responses.
- Schemas (Pydantic) → validação e serialização dos dados de entrada e saída da API.
- Dependencies → gerenciamento de recursos compartilhados da aplicação.
- Services → camada responsável pelas regras de negócio e coordenação dos fluxos da aplicação.
- Repositories → camada responsável pelo acesso e persistência dos dados no banco.
- PostgreSQL → persistência permanente dos dados da aplicação.
- PipefyService → responsável pela integração externa simulada com o Pipefy via GraphQL.
- GraphQL → estrutura utilizada para comunicação com o Pipefy através de mutations.

# Tecnologias utilizadas

### Backend

- FastAPI
Framework principal da API.
- Python
Linguagem utilizada no projeto.
- SQLAlchemy
ORM utilizado para modelagem e persistência no banco.
- Pydantic
Validação de schemas e payloads.

---

### Banco de Dados

- PostgreSQL
Banco de dados principal da aplicação.
- Docker
Utilizado para subir o PostgreSQL em container.
- psycopg2
Driver de conexão entre Python e PostgreSQL.

---

### Testes

- Pytest
Framework de testes automatizados.
- TestClient
Cliente de testes HTTP utilizado nos endpoints.

---

### Integração / APIs

- GraphQL
Utilizado para estruturar as mutations do Pipefy.
- Pipefy
Sistema externo simulado via mutations GraphQL.

---

### Observabilidade / Logging

- Logging nativo do Python (`logging`)

# Estrutura do Projeto

```
client-orchestration-service/
│
├── app/
│   │
│   ├── api/
│   │   │
│   │   ├── dependencies.py         → dependências compartilhadas (DB session)
│   │   │
│   │   └── routes/
│   │       ├── clients.py          → endpoint POST /clientes
│   │       └── webhooks.py         → endpoint POST /webhooks/pipefy/card-updated
│   │
│   ├── core/
│   │   │
│   │   ├── database.py             → engine, session e Base do SQLAlchemy
│   │   └── logger.py               → configuração centralizada de logging
│   │
│   ├── models/
│   │   │
│   │   ├── client.py               → model da tabela clients
│   │   └── processed_event.py      → model da tabela processed_events
│   │
│   ├── repositories/
│   │   │
│   │   ├── client_repository.py    → persistência de clientes
│   │   └── processed_event_repository.py → persistência de eventos processados
│   │
│   │
│   ├── schemas/
│   │   │
│   │   ├── client.py               → schemas de request/response de clientes
│   │   └── webhooks.py             → schemas do webhook Pipefy
│   │
│   ├── services/
│   │   │
│   │   ├── client_service.py       → regras de negócio de clientes
│   │   ├── webhook_service.py      → processamento do webhook
│   │   └── pipefy_services.py      → integração GraphQL simulada
│   │
│   └── main.py                     → inicialização da aplicação FastAPI
│
├── tests/
│   │
│   ├── conftest.py                 → configuração compartilhada dos testes
│   ├── helpers.py                  → builders/helpers de payload
│   │
│   ├── test_clients.py             → testes de criação de clientes
│   └── test_webhooks.py            → testes do fluxo de webhook
│
├── docker-compose.yml              → container PostgreSQL
│
├── requirements.txt                → dependências Python
│
├── .env                            → variáveis de ambiente
│
├── .env.exemplo                    → variáveis de ambiente(exemplo)
│
├── README.md                       → documentação do projeto
│
└── venv/                           → ambiente virtual Python
```

# Como executar o projeto

### Pré-requisitos

Antes de iniciar o projeto, certifique-se de possuir instalado:

- Python 3.10+
- Docker
- Docker Compose

---

### 1. Clonar o repositório

```bash
git clone https://github.com/GabrielLinharesRamos/client-orchestration-service.git
```

```bash
cd client-orchestration-service
```

---

### 2. Criar e ativar ambiente virtual

### Windows

```bash
python -m venv venv
```

```bash
venv\Scripts\activate
```

### Linux / MacOS

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

---

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

---

### 4. Subir o PostgreSQL com Docker

```bash
docker-compose up -d
```

Verifique se o container está rodando:

```bash
docker ps
```

---

### 5. Configurar variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```
DATABASE_URL=postgresql://app_user:app_password@localhost:5432/client_management
```

---

### 6. Executar a aplicação

```bash
uvicorn app.main:app --reload
```

A API ficará disponível em:

```
http://127.0.0.1:8000/
```

---

### 7. Acessar documentação automática

Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

### 8. Executar os testes automatizados

Executar todos os testes:

```bash
pytest
```

Executar um arquivo específico:

```bash
pytest tests/test_clients.py
```

```bash
pytest tests/test_webhooks.py
```

---

### 9. Derrubar containers Docker

```bash
docker-compose down
```

# Exemplos de Requisição

### Exemplo 1 — Criação de Cliente

exemplo de requisição:

```
curl -X POST "http://127.0.0.1:8000/clientes" \
-H "Content-Type: application/json" \
-d '{
  "cliente_nome": "Maria",
  "cliente_email": "maria@example.com",
  "tipo_solicitacao": "Atualização cadastral",
  "valor_patrimonio": 300000
}'
```

Resultado esperado:

```
  {
    "id": (numero identificador),
    "cliente_nome": "Maria",
    "cliente_email": "maria@example.com",
    "tipo_solicitacao": "Atualização cadastral",
    "valor_patrimonio": "300000",
    "status": "Aguardando Análise",
    "prioridade": None
  }
```

### Exemplo 2 — Webhook com Prioridade Alta

```
curl -X POST"http://127.0.0.1:8000/webhooks/pipefy/card-updated" \
-H"Content-Type: application/json" \
-d'{
  "event_id": "evt_001",
  "card_id": "card_001",
  "cliente_email": "maria@example.com",
  "timestamp": "2026-05-18T12:00:00Z"
}'
```

Resultado esperado:

```
{
  "message": "Webhook processado com sucesso",
  "client": {
    "id": (numero identificador),
    "cliente_nome": "Maria",
    "cliente_email": "maria@example.com",
    "tipo_solicitacao": "Atualização cadastral",
    "valor_patrimonio": "300000",
    "status": "Processado",
    "prioridade": "prioridade_alta"
  }
}
```

### Exemplo 3 — Webhook Duplicado (Idempotência)

```
curl -X POST"http://127.0.0.1:8000/webhooks/pipefy/card-updated" \
-H"Content-Type: application/json" \
-d'{
  "event_id": "evt_001",
  "card_id": "card_001",
  "cliente_email": "maria@example.com",
  "timestamp": "2026-05-18T12:00:00Z"
}'
```

Resultado esperado:

```
{
  "detail":"O evento já foi processado"
}
```

# Visão de Produção (AWS)

Caso este projeto fosse executado em ambiente de produção na AWS, a arquitetura seguiria um modelo serverless e event-driven, visando escalabilidade, desacoplamento e resiliência.

O fluxo da aplicação seria:

![phase_3_diagram.drawio.svg](phase_3_diagram.drawio.svg)

### API Gateway

O API Gateway seria responsável por receber as requisições HTTP e encaminhá-las para a Lambda Producer, permitindo escalabilidade automática e integração nativa com serviços serverless.

### Lambda Producer

A Lambda Producer seria responsável por validar e transformar a requisição em um evento de domínio, enviando posteriormente a mensagem para uma fila SQS.

### Amazon SQS

O SQS seria utilizado para permitir processamento assíncrono e desacoplamento entre os componentes da aplicação. Essa abordagem ajuda a absorver picos de tráfego sem sobrecarregar o sistema consumidor.

Além disso, a fila também permitiria retries automáticos em caso de falhas temporárias.

### Dead Letter Queue (DLQ)

Uma Dead Letter Queue seria utilizada para isolar mensagens que falharam múltiplas vezes durante o processamento, aumentando a resiliência do sistema e permitindo análise posterior dos erros.

### Lambda Consumer

A Lambda Consumer seria responsável pelo processamento das mensagens recebidas da fila SQS e persistência dos dados no banco.

Para evitar duplicidade causada por retries da fila, seria implementada idempotência utilizando DynamoDB Conditional Writes.

### DynamoDB

O DynamoDB seria utilizado como banco de dados principal devido à sua baixa latência, alta disponibilidade e escalabilidade horizontal nativa.

### Observabilidade

A observabilidade da aplicação seria realizada utilizando CloudWatch Logs, métricas e alarmes para monitoramento de:

- erros
- latência
- processamento
- mensagens na DLQ

Essa arquitetura permite maior tolerância a falhas, escalabilidade automática e desacoplamento entre os serviços da aplicação.

# DEVLOG

### 24-05-2026:

Hoje foi construída a base da infraestrutura e da arquitetura da aplicação.

---

#### Infraestrutura

Inicialmente, foi criado um container Docker utilizando a imagem do PostgreSQL 16 para servir como banco de dados da aplicação.

Também foi adicionado um arquivo `.env` para armazenar variáveis de ambiente, evitando valores hardcoded no código, como credenciais e URL de conexão do banco de dados.

---

#### Conexão com o banco de dados

Em seguida, foi criado o arquivo `database.py`, responsável pela configuração da conexão com o PostgreSQL através do SQLAlchemy.

Essa camada centraliza:

- criação da engine
- gerenciamento de sessões
- configuração da base ORM

Com isso, a aplicação passou a conseguir se conectar corretamente ao banco de dados.

---

#### Modelagem da entidade Client

Foi criada a model `Client`, representando a tabela de clientes da aplicação.

A tabela é criada automaticamente pelo SQLAlchemy durante a inicialização da aplicação.

Até o momento, a entidade possui campos relacionados às informações do cliente, como:

- nome
- email
- tipo de solicitação
- patrimônio
- status ("Aguardando Análise”)
- prioridade (none)

---

#### Teste inicial da aplicação

Após a configuração da infraestrutura e persistência, foi realizado um teste inicial da aplicação para validar:

- conexão com o banco
- criação automática das tabelas
- funcionamento básico da API

---

#### Schemas com Pydantic

Também foram criados os schemas utilizando Pydantic para validação dos dados de entrada e saída da API.

O schema de entrada é responsável por:

- validar campos obrigatórios
- validar o formato do email
- garantir os tipos corretos dos dados recebidos

Já o schema de resposta adiciona informações geradas pela aplicação, como:

- `id`
- `status`

---

#### Repository Layer

Por fim, foi criada a camada de repository.

Enquanto o `database.py` é responsável por configurar a conexão com o banco de dados, o repository define como os dados poderão ser manipulados dentro da aplicação.

Essa camada será responsável por operações como:

- criação de clientes
- busca por email
- atualização de dados
- consultas futuras

O objetivo dessa separação é manter a arquitetura mais organizada, desacoplada e escalável.

---

#### Diagrama do fluxo da aplicação:

![client_orchestration_diagram.drawio.svg](client_orchestration_diagram.drawio.svg)

A aplicação segue uma arquitetura em camadas:

- Routes: responsáveis pela camada HTTP
- Request Schemas: validar e estruturar os dados recebidos pela API
- Response Schemas: padronizar e serializar os dados retornados pela API.
- Services: regras de negócio
- Repositories: acesso ao banco de dados
- Dependencies: gerenciamento de recursos compartilhados, como sessões do banco

### 25-05-2026:

#### Integração Pipefy (Simulada)

Foi implementada uma camada de serviço dedicada para simular a integração com o Pipefy utilizando GraphQL.

---

#### Pipefy Service

A aplicação possui um `PipefyService` responsável por:

- estruturar a mutation GraphQL `createCard`
- montar dinamicamente o payload enviado ao Pipefy
- simular o envio da requisição
- registrar logs da integração

Exemplo das responsabilidades da camada:

- isolamento da integração externa
- separação entre regra de negócio e comunicação externa
- preparação da aplicação para futuras integrações reais

---

#### Logging

Foi adicionada instrumentação utilizando o módulo `logging` do Python.

Atualmente os logs registram:

- simulação de criação de card no Pipefy
- geração do payload GraphQL
- contexto da operação executada

### 26-05-2026:

#### Processamento de Webhooks e Idempotência

Foi implementado o fluxo responsável pelo processamento de atualizações de cards simuladas via webhook do Pipefy.

A aplicação agora é capaz de:

- receber eventos externos de atualização de card
- validar duplicidade de eventos (`event_id`)
- atualizar o estado do cliente localmente
- aplicar regras de negócio baseadas no patrimônio do cliente
- persistir eventos processados para garantir idempotência

---

#### Webhook Route

Foi criado um novo router dedicado ao processamento de webhooks:

```
POST /webhooks/pipefy/card-updated
```

Responsabilidades da rota:

- receber eventos simulados do Pipefy
- validar payloads de entrada
- encaminhar o processamento para a camada de serviço
- tratar exceções da aplicação

---

#### Webhook Service

Foi implementado o `WebhookService`, responsável por centralizar a lógica de processamento do webhook.

Principais responsabilidades:

- verificar se o `event_id` já foi processado
- buscar clientes utilizando o e-mail recebido no webhook
- aplicar a regra de priorização baseada no patrimônio
- atualizar o status do cliente para `"Processado"`
- coordenar a persistência dos eventos processados

Regras implementadas:

- patrimônio maior ou igual a `200000` → `prioridade_alta`
- patrimônio menor que `200000` → `prioridade_normal`

---

#### Persistência de Eventos Processados

Foi criada uma nova tabela no PostgreSQL:

```
processed_events
```

Objetivo da tabela:

- armazenar eventos já processados
- impedir reprocessamento de webhooks duplicados
- garantir idempotência da aplicação

Campos principais:

- `event_id`
- `client_email`
- `processed_at`

---

#### Repository Layer

Foi implementado o `ProcessedEventRepository`, responsável por:

- consultar eventos já processados
- persistir novos eventos
- isolar regras de acesso ao banco de dados

Além disso, foram adicionadas operações de atualização de clientes já existentes.

---

#### Schemas e Validação

Foram criados novos schemas Pydantic para:

- validação do payload do webhook
- atualização de clientes existentes
- padronização dos dados trafegados entre as camadas da aplicação

As validações garantem:

- formato correto de e-mail
- tipagem consistente
- estrutura adequada dos eventos recebidos

---

#### Arquitetura

A aplicação passou a possuir uma separação mais clara entre:

- rotas HTTP
- regras de negócio
- persistência
- integração externa simulada

Essa estrutura facilita:

- manutenção
- escalabilidade
- testes automatizados
- futuras integrações reais com serviços externos como o Pipefy.

### 27-05-2026:

#### Webhook + Processamento de Eventos

Foi implementado o fluxo completo de processamento de webhooks simulando eventos recebidos do Pipefy.

A aplicação agora possui um endpoint responsável por:

- receber eventos externos
- validar duplicidade de eventos
- aplicar regras de negócio
- atualizar clientes no banco de dados
- simular sincronização com o Pipefy via GraphQL

---

#### Integração Pipefy (Update de Card)

Foi adicionada uma segunda mutation GraphQL simulando atualização de cards no Pipefy.

A nova integração permite:

- estruturar mutations de atualização (`updateCardField`)
- enviar status e prioridade do cliente
- simular sincronização do estado interno com o Pipefy
- registrar logs da operação executada

---

#### Testes Automatizados

Foram implementados testes automatizados cobrindo os principais fluxos da aplicação.

Os testes atualmente validam:

- criação de clientes
- bloqueio de clientes duplicados
- processamento correto do webhook
- cálculo de prioridade alta
- cálculo de prioridade normal
- bloqueio de eventos duplicados (`event_id`)

Também foi criada uma camada de helpers para reutilização de payloads e redução de duplicação nos testes.

---

#### Organização Arquitetural

A aplicação passou a possuir uma separação mais clara entre responsabilidades:

- `Repositories` → persistência de dados
- `Services` → regras de negócio
- `PipefyService` → integração externa simulada
- `Routes` → exposição dos endpoints HTTP

Essa estrutura facilita manutenção, escalabilidade e evolução futura da aplicação.

### 28-05-2026:

### Refatoração da Documentação e Ajustes Gerais

Hoje foi realizada uma refatoração da documentação do projeto, com foco em clareza, organização e melhoria da experiência de utilização da aplicação.

Além disso, também foram corrigidos alguns bugs identificados durante os testes e validações dos fluxos da API.

---

### README

O README foi reorganizado e expandido para refletir melhor a arquitetura e o funcionamento do sistema.

Novas seções adicionadas:

- visão geral da aplicação
- fluxo da aplicação
- tecnologias utilizadas
- estrutura do projeto
- guia de execução local
- exemplos de utilização da API

---

### Correções e Ajustes

Também foram realizados ajustes em partes da aplicação que apresentavam inconsistências durante os testes e execução local.

Entre os ajustes realizados:

- correção de informações incorretas no README
- pequenos bugs relacionados aos fluxos da aplicação
- alinhamento entre documentação e implementação real
- melhorias na consistência dos testes automatizados

### O Bug do "Print Fantasma" (`TypeError` / `KeyError`)

Durante a execução dos testes do webhook, identificou-se que os testes só passavam se houvesse uma instrução `print(client.cliente_email)` logo após a atualização do cliente no serviço. Sem o `print`, a rota falhava ao tentar ler as propriedades `status` e `prioridade` para montar o JSON de resposta, resultando em erros de tipagem.

**Causa Raiz:**
Por padrão, o `sessionmaker` do SQLAlchemy possui a configuração `expire_on_commit=True`. Isso significa que, assim que o método `db.commit()` era executado no repositório, o ORM limpava todos os atributos do objeto `client` na memória para garantir a sincronia com o banco.

- Quando o `print` era executado, o Python forçava uma nova consulta (*lazy loading*) para reidratar o objeto.
- Sem o `print`, o FastAPI tentava serializar o objeto já expirado fora do escopo da transação ativa, quebrando o ciclo de resposta do `TestClient`.

### Resolução e Ajustes na Camada de Core

Para resolver o problema de forma definitiva e seguindo as boas práticas de arquitetura com FastAPI, foram realizadas as seguintes alterações:

- **Configuração do Database (`app/core/database.py`):**
Desativou-se a expiração automática de objetos pós-commit adicionando o parâmetro `expire_on_commit=False` ao `sessionmaker`. Isso garante que os dados persistidos continuem disponíveis na memória para a camada de apresentação (Rotas/Schemas).

Python

```
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False # Mantém o estado do objeto legível pós-commit
)
```
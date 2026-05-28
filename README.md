# Sistema Mundo Invest

banco PostgreSQl rodando em um container Docker

- **`.env`**
- SQLAlchemy conectado
- model Client
- model ProcessedEvent
- tabelas criadas
- **`/health`**
- aplicação sobe sem erro

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
- status
- prioridade

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

### Processamento de Webhooks e Idempotência

Foi implementado o fluxo responsável pelo processamento de atualizações de cards simuladas via webhook do Pipefy.

A aplicação agora é capaz de:

- receber eventos externos de atualização de card
- validar duplicidade de eventos (`event_id`)
- atualizar o estado do cliente localmente
- aplicar regras de negócio baseadas no patrimônio do cliente
- persistir eventos processados para garantir idempotência

---

### Webhook Route

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

### Webhook Service

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

### Persistência de Eventos Processados

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

### Repository Layer

Foi implementado o `ProcessedEventRepository`, responsável por:

- consultar eventos já processados
- persistir novos eventos
- isolar regras de acesso ao banco de dados

Além disso, foram adicionadas operações de atualização de clientes já existentes.

---

### Schemas e Validação

Foram criados novos schemas Pydantic para:

- validação do payload do webhook
- atualização de clientes existentes
- padronização dos dados trafegados entre as camadas da aplicação

As validações garantem:

- formato correto de e-mail
- tipagem consistente
- estrutura adequada dos eventos recebidos

---

### Arquitetura

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

### 28-05-2026:

#### Webhook + Processamento de Eventos

Foi implementado o fluxo completo de processamento de webhooks simulando eventos recebidos do Pipefy.

A aplicação agora possui um endpoint responsável por:

- receber eventos externos
- validar duplicidade de eventos
- aplicar regras de negócio
- atualizar clientes no banco de dados
- simular sincronização com o Pipefy via GraphQL

---

#### Idempotência de Eventos

Foi criada a tabela `processed_events` para garantir idempotência no processamento de webhooks.

A estratégia implementada consiste em:

- verificar se um `event_id` já foi processado
- bloquear reprocessamentos duplicados
- registrar eventos consumidos no banco local

Essa abordagem evita inconsistências causadas por múltiplos envios do mesmo webhook.

---

#### Regras de Negócio

O webhook agora aplica regras de priorização baseadas no patrimônio do cliente:

- patrimônio maior ou igual a `200000` → `prioridade_alta`
- patrimônio menor que `200000` → `prioridade_normal`

Além disso:

- o status do cliente é atualizado para `Processado`
- a prioridade calculada é persistida no banco

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
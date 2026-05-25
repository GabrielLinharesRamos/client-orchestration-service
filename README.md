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
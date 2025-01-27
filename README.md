# API de Consulta de Regiões por Número de Telefone

Essa é uma API simples construída com Python no framework FastAPI. Sua funcionalidade principal é retornar a região associada ao DDD de um número de telefone fornecido. 

A API também possui uma rota que lista todos os DDDs e suas respectivas regiões no Brasil.

## Funcionalidades

- **Listar DDDs**: Retorna todos os DDDs com suas respectivas regiões no Brasil.
- **Consultar Região**: Recebe um número de telefone e retorna a região correspondente ao DDD.

## Pré-requisitos

- Python 3.8 ou superior

## Instalação

1. Clone o repositório em sua máquina:

   ```bash
   git clone <url-do-repositorio>
   cd <nome-do-repositorio>
   ```

2. Crie e ative um ambiente virtual:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # No Windows: .venv\Scripts\activate
   ```

3. Instale as dependências listadas no `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

## Executando a API

1. Inicie o servidor usando o Uvicorn:

   ```bash
   uvicorn main:app --host 0.0.0.0 --port 3003
   ```

2. Acesse a documentação interativa da API em seu navegador:

   - [http://localhost:3003/docs](http://localhost:3003/docs) (Swagger UI)
   - [http://localhost:3003/redoc](http://localhost:3003/redoc) (ReDoc)

## Rotas

### `GET /ddds`
Retorna todos os DDDs com suas respectivas regiões no Brasil.

#### Exemplo de resposta:
```json
{
  "11": "São Paulo",
  "21": "Rio de Janeiro",
  "31": "Belo Horizonte"
}
```

### `POST /regiao`
Recebe um número de telefone e retorna a região correspondente ao DDD.

#### Corpo da requisição:
```json
{
  "telefone": "11987654321"
}
```

#### Exemplo de resposta:
```json
{
  "ddd": "11",
  "regiao": "São Paulo"
}
```

## Tratamento de CORS
O suporte a CORS é habilitado na API para garantir a comunicação com outros domínios.


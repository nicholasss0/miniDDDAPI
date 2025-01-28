# API de Consulta de Região por Número de Telefone

Esta é uma API simples desenvolvida em Python utilizando o framework **FastAPI**. Ela retorna a região do Brasil com base no número de telefone recebido (a partir do DDD) ou apresenta uma lista de todos os DDDs e suas respectivas regiões.

## Funcionalidades

- **Rota 1:** Listar todos os DDDs e suas regiões no Brasil.
- **Rota 2:** Receber um número de telefone e retornar a região correspondente ao DDD.

A API roda na porta **3003** e conta com correção de CORS mediada pelo **Uvicorn**.

---

## Instalação e Uso

Siga os passos abaixo para configurar e rodar a API em sua máquina local:

### Pré-requisitos
- Python 3.8 ou superior
- Gerenciador de pacotes `pip`

### Passo 1: Clonar o Repositório

Clone este repositório em sua máquina local:
```bash
git clone <URL_DO_REPOSITORIO>
cd <NOME_DO_REPOSITORIO>
```

### Passo 2: Criar um Ambiente Virtual

Crie um ambiente virtual para isolar as dependências do projeto:
```bash
python -m venv .venv
```
Ative o ambiente virtual:
- No Windows:
  ```bash
  .venv\Scripts\activate
  ```
- No Linux/macOS:
  ```bash
  source .venv/bin/activate
  ```

### Passo 3: Instalar Dependências

Instale as dependências listadas no arquivo `requirements.txt`:
```bash
pip install -r requirements.txt
```

### Passo 4: Rodar a API

A API inicia o servidor local automaticamente utilizando o Uvicorn, 
bastando apenas executar o script main.py:

```bash
python main.py
```

A API estará disponível em `http://127.0.0.1:3003`.

---

## Endpoints

### 1. **Obter todos os DDDs e regiões**
**Rota:** `/ddds`

**Método:** `GET`

**Descrição:** Retorna um JSON com todos os DDDs e suas respectivas regiões no Brasil.

**Exemplo de Resposta:**
```json
{
  "11": "São Paulo",
  "21": "Rio de Janeiro",
  "61": "Distrito Federal"
//   ...
}
```

### 2. **Consultar região por número de telefone**
**Rota:** `/regiao`

**Método:** `POST`

**Descrição:** Recebe um número de telefone e retorna a região correspondente ao DDD.

**Exemplo de Requisição:**
```json
{
  "telefone": "11987654321"
}
```

**Exemplo de Resposta:**
```json
{
  "regiao": "São Paulo"
}
```
---

## Testando a API

O projeto tem um arquivo **templates/index.html** para testar o funcionamento da API, 
basta carregá-lo no navegador

---

## Licença
Este projeto um código aberto. Sinta-se à vontade para baixá-lo, utilizá-lo e modificá-lo conforme necessário.


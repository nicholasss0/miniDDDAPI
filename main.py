from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
import uvicorn

app = FastAPI()

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuração do JWT
SECRET_KEY = "secret-key-para-mudar"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

DDD_REGIONS = {
    "11": "São Paulo (Capital e Grande São Paulo)",
    "12": "São Paulo (Litoral Norte)",
    "13": "São Paulo (Baixada Santista)",
    "14": "São Paulo (Noroeste Paulista)",
    "15": "São Paulo (Sudoeste Paulista)",
    "16": "São Paulo (Nordeste Paulista)",
    "17": "São Paulo (Interior de São Paulo)",
    "18": "São Paulo (Interior Sul)",
    "19": "São Paulo (Campinas)",
    "21": "Rio de Janeiro (Capital e Grande Rio)",
    "22": "Rio de Janeiro (Interior Fluminense)",
    "24": "Rio de Janeiro (Norte Fluminense)",
    "27": "Espírito Santo (Capital e Interior)",
    "28": "Espírito Santo (Interior Sul)",
    "31": "Minas Gerais (Belo Horizonte e Região Metropolitana)",
    "32": "Minas Gerais (Zona da Mata)",
    "33": "Minas Gerais (Leste de Minas)",
    "34": "Minas Gerais (Triângulo Mineiro e Alto Paranaíba)",
    "35": "Minas Gerais (Sul de Minas)",
    "37": "Minas Gerais (Centro-Oeste de Minas)",
    "38": "Minas Gerais (Norte de Minas)",
    "41": "Paraná (Curitiba e Região Metropolitana)",
    "42": "Paraná (Centro-Sul)",
    "43": "Paraná (Norte do Paraná)",
    "44": "Paraná (Oeste do Paraná)",
    "45": "Paraná (Sudoeste do Paraná)",
    "46": "Paraná (Noroeste do Paraná)",
    "47": "Santa Catarina (Florianópolis e Região Metropolitana)",
    "48": "Santa Catarina (Sul de Santa Catarina)",
    "49": "Santa Catarina (Oeste e Planalto)",
    "51": "Rio Grande do Sul (Porto Alegre e Região Metropolitana)",
    "53": "Rio Grande do Sul (Sul e Zona Sul)",
    "54": "Rio Grande do Sul (Serra Gaúcha)",
    "55": "Rio Grande do Sul (Centro e Norte)",
    "61": "Distrito Federal (Brasília e Região Metropolitana)",
    "62": "Goiás (Goiânia e Região Metropolitana)",
    "63": "Tocantins (Capital e Interior)",
    "64": "Goiás (Interior de Goiás)",
    "65": "Mato Grosso (Cuiabá e Região Metropolitana)",
    "66": "Mato Grosso (Interior de Mato Grosso)",
    "67": "Mato Grosso do Sul (Campo Grande e Região Metropolitana)",
    "68": "Acre (Capital e Interior)",
    "69": "Rondônia (Porto Velho e Interior)",
    "71": "Bahia (Salvador e Região Metropolitana)",
    "73": "Bahia (Interior da Bahia)",
    "74": "Bahia (Centro-Sul da Bahia)",
    "75": "Bahia (Sul da Bahia)",
    "77": "Bahia (Extremo Sul da Bahia)",
    "79": "Sergipe (Capital e Interior)",
    "81": "Pernambuco (Recife e Região Metropolitana)",
    "82": "Alagoas (Maceió e Interior)",
    "83": "Paraíba (João Pessoa e Interior)",
    "84": "Rio Grande do Norte (Natal e Região Metropolitana)",
    "85": "Ceará (Fortaleza e Região Metropolitana)",
    "86": "Piauí (Teresina e Interior)",
    "87": "Pernambuco (Interior de Pernambuco)",
    "88": "Ceará (Interior do Ceará)",
    "89": "Piauí (Interior do Piauí)",
    "91": "Pará (Belém e Região Metropolitana)",
    "92": "Amazonas (Manaus e Região Metropolitana)",
    "93": "Pará (Interior do Pará)",
    "94": "Pará (Nordeste do Pará)",
    "95": "Roraima (Capital e Interior)",
    "96": "Amapá (Capital e Interior)",
    "97": "Maranhão (São Luís e Interior)",
    "98": "Maranhão (Interior do Maranhão)",
    "99": "Maranhão (Oeste do Maranhão)"
}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Banco de usuários fixo para exemplo (em produção, utilize hash de senha)
fake_users_db = {
    "admin": {
        "username": "admin",
        "password": "1234"  # Em produção, armazene o hash da senha
    }
}

# Configuração do hash de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Funções auxiliares


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_user(db, username: str):
    return db.get(username)


def authenticate_user(username: str, password: str):
    user = get_user(fake_users_db, username)
    # Se for utilizar hash, descomente a linha abaixo e armazene o hash em fake_users_db:
    # if not user or not verify_password(password, user["password"]):
    if not user or user["password"] != password:
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)



@app.get("/generate_token")
async def generate_token():
    token = create_access_token(data={"sub": "admin"})
    return {"access_token": token, "token_type": "bearer"}


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None or username not in fake_users_db:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais inválidas"
            )
        return username
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )

# Rota para obter token JWT


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Dicionário de DDDs


@app.get("/region/{phone_number}")
async def get_region(phone_number: str, current_user: str = Depends(get_current_user)):
    ddd = phone_number[:2]
    if ddd in DDD_REGIONS:
        return {"ddd": ddd, "region": DDD_REGIONS[ddd]}
    return {"error": "DDD não encontrado"}


@app.get("/ddds")
async def get_ddds(current_user: str = Depends(get_current_user)):
    return DDD_REGIONS

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3003)

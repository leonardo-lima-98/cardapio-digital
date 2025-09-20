```

## 16. README.md

```markdown
# Sistema de Cardápios Digitais

Sistema completo para criação e gerenciamento de cardápios digitais usando FastAPI.

## 🚀 Funcionalidades

- ✅ **Autenticação JWT** para área administrativa
- ✅ **CRUD completo** para restaurantes, categorias e itens
- ✅ **API pública** para consulta do cardápio
- ✅ **Suporte a SQLite** (desenvolvimento) e **PostgreSQL** (produção)
- ✅ **Migrações com Alembic**
- ✅ **Docker** e **Docker Compose**
- ✅ **Estrutura organizada** em módulos

## 📁 Estrutura do Projeto

```
cardapio-digital/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── security.py
│   │   └── database.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── session.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── restaurant.py
│   │   ├── category.py
│   │   └── item.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── restaurant.py
│   │   ├── category.py
│   │   ├── item.py
│   │   └── token.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── admin/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── restaurants.py
│   │   │   ├── categories.py
│   │   │   └── items.py
│   │   └── menu.py
│   └── middleware/
│       ├── __init__.py
│       └── auth.py
├── alembic/
│   ├── versions/
│   ├── env.py
│   ├── script.py.mako
│   └── alembic.ini
├── requirements.txt
├── .env
├── .env.example
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## 🛠️ Instalação e Execução

### Desenvolvimento Local

1. **Clone o repositório**
```bash
git clone <repo-url>
cd digital-menu-system
```

2. **Crie um ambiente virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente**
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

5. **Execute as migrações**
```bash
alembic upgrade head
```

6. **Crie dados de exemplo** (opcional)
```bash
python scripts/init_db.py
```

7. **Execute a aplicação**
```bash
uvicorn app.main:app --reload
```

### Com Docker

1. **Desenvolvimento**
```bash
docker-compose -f docker-compose.dev.yml up --build
```

2. **Produção**
```bash
docker-compose up --build -d
```

## 📋 Uso da API

### Autenticação

1. **Registrar usuário**
```bash
POST /admin/auth/register
{
  "name": "João Silva",
  "email": "joao@exemplo.com",
  "password": "senha123"
}
```

2. **Login**
```bash
POST /admin/auth/login
{
  "email": "joao@exemplo.com",
  "password": "senha123"
}
```

### Gestão de Restaurantes

```bash
# Criar restaurante (requer autenticação)
POST /admin/restaurants/
Authorization: Bearer <token>
{
  "name": "Meu Restaurante",
  "address": "Rua das Flores, 123",
  "phone": "(48) 99999-9999"
}
```

### Consulta Pública do Cardápio

```bash
GET /menu/?id=<restaurant_uuid>
```

Retorna o cardápio completo com informações do restaurante, categorias e itens.

## 🗄️ Banco de Dados

### Modelos

- **User**: Usuários do sistema (donos de restaurantes)
- **Restaurant**: Restaurantes cadastrados
- **Category**: Categorias do cardápio (ex: Sanduíches, Bebidas)
- **Item**: Itens do cardápio (produtos)

### Migrações

```bash
# Criar nova migração
alembic revision --autogenerate -m "Descrição da mudança"

# Aplicar migrações
alembic upgrade head

# Voltar migração
alembic downgrade -1
```

## 🔧 Configurações

As configurações são gerenciadas via arquivo `.env`:

```env
DEBUG=true                                    # Modo debug
SECRET_KEY=sua-chave-secreta                 # Chave JWT
DATABASE_URL=sqlite:///./digital_menu.db     # URL do banco
ACCESS_TOKEN_EXPIRE_MINUTES=30               # Expiração do token
```

## 📚 Documentação da API

Após iniciar a aplicação, acesse:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔐 Segurança

- Senhas são criptografadas com bcrypt
- Autenticação via JWT
- Middleware de autenticação para rotas administrativas
- Validação de propriedade de recursos

## 🐳 Docker

### Desenvolvimento
```bash
docker-compose -f docker-compose.dev.yml up
```

### Produção
```bash
docker-compose up -d
```

## 📝 Exemplo de Uso

1. Registre um usuário
2. Faça login e obtenha o token
3. Crie um restaurante
4. Adicione categorias ao restaurante  
5. Adicione itens às categorias
6. Acesse o cardápio público via `/menu/?id=<restaurant_id>`

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT.
```

## Como Executar

1. **Crie a estrutura de pastas** conforme mostrado acima
2. **Copie cada arquivo** para sua respectiva pasta
3. **Configure o ambiente**:
   ```bash
   cp .env.example .env
   # Edite o .env com suas configurações
   ```
4. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```
5. **Execute as migrações**:
   ```bash
   alembic upgrade head
   ```
6. **Crie dados de exemplo**:
   ```bash
   python scripts/init_db.py
   ```
7. **Execute a aplicação**:
   ```bash
   uvicorn app.main:app --reload
   ```

O sistema estará disponível em `http://localhost:8000` com documentação automática em `/docs`.
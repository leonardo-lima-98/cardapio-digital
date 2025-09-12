# 🍽️ Cardápio Digital

Um sistema simples que o cliente do restaurante lê o QR Code e sistema serve cardápios digitais .

---

## 🚀 Funcionalidades

- Criar cardápio para restaurante.
- Adicionar categorias/sessões (ex: Massas, Combos, Porçao Extra, Bebidas, ...).
- Adicionar produtos dentro de categorias.
- Listar todos os restaurantes cadastrados (`/`).
- Recuperar cardápio via QR Code (`/menu/{id_restaurante}`).
- Persistência em arquivos JSON (sem banco de dados).

---

## 🛠️ Instalação

### Pré-requisitos
- [Docker](https://docs.docker.com/get-docker/)  
- [Docker Compose](https://docs.docker.com/compose/install/) (opcional)

### Passos
```bash
# Clone o repositório
git clone https://github.com/leonardo-lima-98/cardapio-digital.git
cd cardapio-digital

# Build da imagem
docker build -t cardapio-digital .

# Rodar o container
docker run -p 8000:8000 cardapio-digital
```

A API estará disponível em:  
👉 [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📂 Estrutura do projeto

```
cardapio-digital/
 ├── data/              # Cardápios em JSON
 ├── src/
 │    ├── schemas.py    # Modelos Pydantic
 │    ├── utils.py      # Funções auxiliares
 │    └── main.py       # Rotas FastAPI
 ├── requirements.txt   # Dependências
 ├── Dockerfile         # Configuração Docker
 └── README.md
```

---

## ✅ Exemplo de Uso

- **Listar restaurantes**
```bash
GET /
```

- **Criar cardápio**
```bash
POST /menu?titulo=Cardápio&nome_restaurante=XPTO
```

- **Adicionar categoria**
```bash
POST /menu/{id}/categorias?categorias=Massas,Bebidas
```

- **Adicionar produto**
```bash
POST /menu/{id}/categoria/Massas/produto
{
  "nome": "Massa ao molho",
  "descricao": "Massa com molho",
  "preco": 30,
  "imagem": "massa.jpg"
}
```

---

### [📌 TODO List – Próximos Passos ↗️](/TODO.md)  


- 🔐 Área Admin
- 🗄️ Banco de Dados
- 🧑‍💻 Middleware
- ⚡ Performance

---

## 👨‍💻 Autor
Projeto criado para aprendizado e prototipação de um **Cardápio Digital** em FastAPI.

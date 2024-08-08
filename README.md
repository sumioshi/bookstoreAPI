
```markdown
# Bookstore API

Bem-vindo à API da Livraria! Este projeto é uma API construída com Django e Django REST Framework para gerenciar uma coleção de livros.

## Funcionalidades

- Listar livros
- Adicionar livros
- Atualizar livros
- Remover livros

## Requisitos

- Python 3.12
- Poetry

## Configuração do Ambiente

### 1. Clonar o Repositório

Clone o repositório do GitHub para a sua máquina local:

```sh
git clone https://github.com/usuario/bookstore.git
cd bookstore
```

### 2. Instalar Dependências

Use o Poetry para instalar todas as dependências do projeto:

```sh
poetry install
```

### 3. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto e adicione as seguintes variáveis de ambiente:

```env
DEBUG=True
SECRET_KEY=sua-chave-secreta
```

### 4. Aplicar Migrações

Aplique as migrações para configurar o banco de dados:

```sh
poetry run python manage.py makemigrations
poetry run python manage.py migrate
```

### 5. Executar o Servidor de Desenvolvimento

Inicie o servidor de desenvolvimento do Django:

```sh
poetry run python manage.py runserver
```

Acesse a aplicação no navegador em `http://127.0.0.1:8000/`.

## Estrutura do Projeto

```plaintext
bookstore/
├── api/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── bookstore/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── views.py
│   ├── wsgi.py
├── templates/
│   └── index.html
├── manage.py
└── pyproject.toml
```

## Endpoints da API

A API oferece os seguintes endpoints:

- `GET /api/books/` - Lista todos os livros
- `POST /api/books/` - Adiciona um novo livro
- `GET /api/books/{id}/` - Detalhes de um livro específico
- `PUT /api/books/{id}/` - Atualiza um livro específico
- `DELETE /api/books/{id}/` - Remove um livro específico

## Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b minha-feature`)
3. Commit suas alterações (`git commit -am 'Adiciona minha feature'`)
4. Push para a branch (`git push origin minha-feature`)
5. Abra um Pull Request


Aqui está a documentação atualizada incluindo a correção da versão do Python na build:

---

# 🛠️ DOCUMENTATION.md

## 🚀 Resolvendo Problemas na Build e Testes

### Contexto
Durante o desenvolvimento na branch `demo-github-actions`, encontramos alguns problemas tanto na execução dos testes locais quanto na pipeline do GitHub Actions. Abaixo, explico de forma simples como resolvemos tudo isso. 😉

---

### 🐛 Problema 1: Falha na Build do GitHub Actions

#### 🚨 O Que Aconteceu?
A pipeline do GitHub Actions estava falhando ao rodar os testes, com o erro `ModuleNotFoundError: No module named 'whitenoise'`. Além disso, havia um problema relacionado à versão do Python utilizada na build.

#### 🔍 Por Que Isso Aconteceu?
1. O módulo `whitenoise`, essencial para o Django, não estava listado como dependência no arquivo de configuração (`pyproject.toml`). Por isso, ele não foi instalado no ambiente do GitHub Actions.
2. A versão do Python configurada na pipeline do GitHub Actions era 3.9, enquanto o projeto estava sendo desenvolvido na versão 3.12 localmente, o que causava inconsistências.

#### 🛠️ Como Corrigimos?
1. **Arquivo**: `pyproject.toml`
   - **Antes**:
     ```toml
     [tool.poetry.dependencies]
     python = "^3.12"
     Django = "^3.2"
     ```
   - **Depois**:
     ```toml
     [tool.poetry.dependencies]
     python = "^3.12"
     Django = "^3.2"
     whitenoise = "^6.0"
     ```
   - Executamos o comando para adicionar `whitenoise` como dependência:
     ```bash
     poetry add whitenoise
     ```

2. **Arquivo**: `build.yml` (configuração da pipeline do GitHub Actions)
   - **Antes**:
     ```yaml
     - name: Set up Python 3.9
       uses: actions/setup-python@v2
       with:
         python-version: 3.9
     ```
   - **Depois**:
     ```yaml
     - name: Set up Python 3.12
       uses: actions/setup-python@v2
       with:
         python-version: 3.12
     ```

#### ✅ Resultado
Com `whitenoise` listado corretamente como dependência e a versão do Python ajustada para 3.12 na pipeline, a build passou a funcionar corretamente e os testes foram executados com sucesso! 🎉

---

### 🐍 Problema 2: Erros nos Arquivos Python e SQL

#### 🚨 O Que Aconteceu?
Os testes locais estavam falhando ao tentar se conectar ao banco de dados e ao carregar arquivos SQL. Isso resultava em erros de encoding e variáveis de ambiente mal configuradas.

#### 🔍 Por Que Isso Aconteceu?
As variáveis de ambiente no `settings.py` não estavam sendo carregadas corretamente, resultando em valores `None` para as configurações do banco de dados.

#### 🛠️ Como Corrigimos?
1. **Arquivo**: `settings.py`
   - **Antes**:
     ```python
     DATABASES = {
         "default": {
             "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
             "NAME": os.environ.get("SQL_DATABASE", BASE_DIR / "db.sqlite3"),
             "USER": os.environ.get("SQL_USER", "user"),
             "PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
             "HOST": os.environ.get("SQL_HOST", "localhost"),
             "PORT": os.environ.get("SQL_PORT", "5432"),
         }
     }
     ```
   - **Depois**:
     Configuramos corretamente as variáveis de ambiente usando `python-decouple`:
     ```python
     from decouple import config

     DATABASES = {
         "default": {
             "ENGINE": config("SQL_ENGINE", "django.db.backends.sqlite3"),
             "NAME": config("SQL_DATABASE", BASE_DIR / "db.sqlite3"),
             "USER": config("SQL_USER", "user"),
             "PASSWORD": config("SQL_PASSWORD", "password"),
             "HOST": config("SQL_HOST", "localhost"),
             "PORT": config("SQL_PORT", "5432"),
         }
     }
     ```

#### ✅ Resultado
Após essas mudanças, os testes locais passaram a se conectar ao banco de dados corretamente e os arquivos SQL foram carregados sem problemas! Tudo rodando perfeitamente. 🚀

---

### Lista de Comandos Usados

1. **Rodar as migrações no Django:**
   ```bash
   python manage.py migrate
   ```

2. **Verificar status do Git:**
   ```bash
   git status
   ```

3. **Executar migrações no container Docker:**
   ```bash
   docker-compose exec web python manage.py migrate
   ```

4. **Subir os containers Docker:**
   ```bash
   docker-compose up -d
   ```

5. **Executar o servidor Django:**
   ```bash
   python manage.py runserver
   ```

6. **Executar os testes no container Docker:**
   ```bash
   docker-compose exec web python manage.py test
   ```

7. **Executar os testes localmente:**
   ```bash
   python manage.py test
   ```

8. **Adicionar todos os arquivos ao stage no Git:**
   ```bash
   git add .
   ```

9. **Verificar o status do Git novamente após o `git add`:**
   ```bash
   git status
   ```

10. **Commitar as mudanças no Git:**
    ```bash
    git commit -m "Documenta a resolução dos problemas na branch demo-github-actions"
    ```

11. **Enviar as mudanças para o repositório remoto:**
    ```bash
    git push origin demo-github-actions
    ```

12. **Atualizar as dependências do Poetry com `whitenoise`:**
    ```bash
    poetry add whitenoise
    ```

13. **Bloquear as dependências no Poetry após adicionar `whitenoise`:**
    ```bash
    poetry lock
    ```

14. **Executar os testes usando o Poetry:**
    ```bash
    poetry run python manage.py test
    ```

15. **Trocar para a branch `main`:**
    ```bash
    git checkout main
    ```

16. **Puxar as últimas mudanças da branch `main`:**
    ```bash
    git pull origin main
    ```

17. **Fazer o merge da branch `demo-github-actions` na `main`:**
    ```bash
    git merge demo-github-actions
    ```

18. **Enviar as mudanças para a branch `main` no repositório remoto:**
    ```bash
    git push origin main
    ```

---

### Conclusão
Após seguir todos esses passos e executar todos esses comandos, chegamos ao ponto em que a build no GitHub Actions foi bem-sucedida e os testes rodaram corretamente tanto localmente quanto no ambiente de CI/CD.


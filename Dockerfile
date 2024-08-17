# `python-base` sets up all our shared environment variables
FROM python:3.12-slim as python-base

# python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.0.3 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        build-essential \
        zlib1g-dev \
        libjpeg-dev \
        libfreetype6-dev \
        liblcms2-dev \
        libopenjp2-7-dev \
        libtiff5-dev \
        libwebp-dev \
        tcl8.6-dev \
        tk8.6-dev \
        python3-tk \
        libharfbuzz-dev \
        libfribidi-dev \
        libxcb1-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Debug step: Check Python and pip versions
RUN python --version && pip --version

# install poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN pip install poetry

# Debug step: Check Poetry installation
RUN poetry --version

# install postgres dependencies inside of Docker
RUN apt-get update && apt-get install -y locales \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2 \
    && echo "en_US.UTF-8 UTF-8" > /etc/locale.gen \
    && locale-gen en_US.UTF-8 \
    && update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8

# Debug step: Check installed packages
RUN pip list

# copy project requirement files here to ensure they will be cached.
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./

# Debug step: List contents of the working directory
RUN ls -al /opt/pysetup

# install runtime deps - uses $POETRY_VIRTUALENVS_IN_PROJECT internally
RUN poetry install --no-dev

# Debug step: List installed packages after poetry install
RUN poetry show

# quicker install as runtime deps are already installed
RUN poetry install

WORKDIR /app

COPY . /app/

# Debug step: List contents of /app directory
RUN ls -al /app

RUN poetry install --no-dev && poetry show gunicorn

EXPOSE 8000

# Use gunicorn to serve the application
CMD ["gunicorn", "bookstore.wsgi:application", "--bind", "0.0.0.0:8000"]

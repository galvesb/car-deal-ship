FROM python:3.9-slim as builder

RUN mkdir -p /app
WORKDIR /app

# Aquivo de dependências
ADD requirements.txt .
ADD requirements ./requirements/

# Repositório extra a utilizar
ARG PIP_EXTRA_INDEX_URL

RUN python3 -m venv venv \
    && venv/bin/python -m pip install pip setuptools wheel --no-cache-dir --upgrade \
    && venv/bin/python -m pip install --no-cache-dir -r requirements.txt

ADD . .

FROM python:3.9-slim

# Envs
ENV HOME="/app"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/${HOME}/venv/bin:$PATH"
ENV PYTHONPATH "${PYTHONPATH}:${HOME}"
ENV PORT 5000

# Cria e define o diretório padrão de trabalho
RUN mkdir -p ${HOME}
WORKDIR ${HOME}

# Copia o código fonte da aplicação
COPY --from=builder ${HOME} ${HOME}

# Cria o grupo, usuário e prepara o venv
RUN addgroup --quiet --gid 2000 cardealship \
    && useradd cardealship --uid=2000 --gid=2000 --home-dir ${HOME} --no-create-home --shell /bin/bash \
    && chown -R cardealship:cardealship ${HOME}

# Define o usuário padrão para essa imagem
USER cardealship
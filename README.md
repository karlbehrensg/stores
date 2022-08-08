<div align="center">
  <h1>User registration in microservice with FastAPI</h1>
</div>

# Introduction

This repository contains a base project to develop a microservice with FastAPI. The objective of this repository is to structure a base project in FastAPI. This project establishes the necessary folder structure for the domain and services layers, in addition to the tests, in this way, the development stage is simplified so that it focuses on what is really necessary.

# Table of Contents

- [Install dependencies](#install-dependencies)
- [Set environment variables](#set-environment-variables)
- [Create Models](#create-models)
- [Migrations](#migrations)
  - [Create migrations](#create-migrations)
    - [Automatic](#automatic)
    - [Manual](#manual)
  - [Apply migrations](#apply-migrations)
  - [Downgrade migrations](#downgrade-migrations)
- [API entrypoints](#api-entrypoints)
- [Schemas](#schemas)
- [Run server](#run-server)
  - [Development](#development)
  - [Production](#production)
- [Test](#tests)

# Docker

To create de docker image variables must be determined:

```bash
SECRET="my-secret-key"
DB_DIALECT="postgresql"
DB_HOST="localhost"
DB_PORT="5432"
DB_NAME="postgres"
DB_USER="postgres"
DB_PASSWORD="postgres"
```

After the variables are determined you can build the image:

```bash
docker build -t stores .
```

To execute the new image you must use the variables determined before:

```bash
docker run -d -e SECRET="my-secret-key" -e DB_DIALECT="postgresql" -e DB_HOST="stores_db" -e DB_PORT="5432" -e DB_NAME="postgres" -e DB_USER="postgres" -e DB_PASSWORD="postgres" --network zeleri --name stores -p 83:80 stores
```
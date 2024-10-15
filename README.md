# Wrapper Geocode Reverse

## Motivação

Wrapper Geocode Reverse é uma api de comunicação com a api da Open Router Service, feito em python, com o intuito de possibilitar que uma pessoa/empresa forneça este recurso para varias pessoas utilizando somente uma key fornecida pela Open router service.
O seu desenvolvimento o ocorreu da solicitação de uma feature que possibilitava os clientes obterem o endereço na hora de realizar o cadastro através da sua localização. Num primeiro ponto foi tido a ideia de utilizar o *Open Router Service*, mas era inviável criar e atualizar e controlar a key utilizada para cada cliente que utilizaria o sistema. E criar uma key para a empresa tornaria um problema caso vários clientes tentassem obter o endereço, visto que poderia bloquear o uso por alguns minutos segundo o termo de uso da ORS.
Com isto foi decido criar está api para ser intermediador entre o uso do cliente e o sistema da ORS, controlando as requisições e verificando se aquela localização já foi buscada e acessando o banco local da API, evitando o consumo desnecessário do recurso na ORS e assim pode utilizar uma API key para cada empresa que utiliza o sistema.

## Indices

- [Wrapper Geocode Reverse](#wrapper-geocode-reverse)
  - [Motivação](#motivação)
  - [Indices](#indices)
  - [Requerimentos](#requerimentos)
  - [Rodar a aplicação](#rodar-a-aplicação)
  - [Para teste da aplicação](#para-teste-da-aplicação)
  - [Caso prefira pode subir a aplicação via Docker Compose](#caso-prefira-pode-subir-a-aplicação-via-docker-compose)
  - [Executar os teste](#executar-os-teste)
    - [Parar o Container da aplicação](#parar-o-container-da-aplicação)
      - [Parar aplicação](#parar-aplicação)
      - [Parar e remover o Container](#parar-e-remover-o-container)
  - [Possíveis erros](#possíveis-erros)
  - [Referencias](#referencias)

## Requerimentos

- [Python](https://www.python.org/downloads/release/python-3123/) - 3.12.3
- [Pyenv](https://github.com/pyenv/pyenv) (Opcional)
- [Poetry](https://python-poetry.org/) - latest
- [Docker](https://registry.hub.docker.com/r/postgis/postgis/) - latest
- [Postgis](https://registry.hub.docker.com/r/postgis/postgis/) - latest

> [!WARNING]
> Os comandos de **Docker** utilizado estão baseados na versão 2.0

## Rodar a aplicação

1. **Clone o Repository:**

    ```bash
    git clone https://github.com/RobertsFerreira/wrapper_geocode_reverse.git
    cd wrapper_geocode_reverse
    ```

2. **Instalar e selecionado versão do python no pyenv:**

    ```bash
    pyenv list
    pyenv install 3.12.3
    ```

    ```bash
    pyenv local 3.12.3
    ```

3. **Instalar dependências**

    ```bash
    poetry shell
    poetry install
    poetry update
    ```

4. **Subir Banco de dados**

    ```bash
    docker run --name some-postgis -e POSTGRES_PASSWORD=mysecretpassword -e POSTGRES_DB=postgres -d postgis/postgis
    ```

5. **Criação .env**
   Criar um arquivo **.env** baseado no **.env.txt**

6. **Configuração do .env**

    Adicione as informações nos seguintes campos abaixo

   ```bash
    # database
    DATABASE_URL=

    # Postgis
    POSTGRES_USER=
    POSTGRES_DB=
    POSTGRES_PASSWORD=

    # openrouter
    OPEN_ROUTER_TOKEN=
   ```

   O **OPEN_ROUTER_TOKEN** é o token gerado dentro da conta no site do [Open Router Service](https://openrouteservice.org/)

   > [!NOTE]
   > O database url segue o padrão utilizado pelo sqlachelmy
   >
   > "postgresql+psycopg://user:password@host:port/database"

7. **Rodar migrations**

    ```bash
    poetry shell
    alembic upgrade head
    ```

8. **Executar aplicação**

    ```bash
    poetry shell
    task run
    ```

## Para teste da aplicação

   ![Exemplo de console após rodar o start da aplicação](.github/images/cmd_running.png)
   Para tester pode utilizar o **/docs** utilizando o *localhost* -> **127.00.0.1:8080/docs**

   ![Exemplo do swagger de documentação](.github/images/example_swagger.png)

## Caso prefira pode subir a aplicação via Docker Compose

> [!NOTE]
> Irá ser necessário o arquivo .env

1. **Criação .env**
   Criar um arquivo **.env** baseado no **.env.txt**

2. **Configuração do .env**

    Adicione as informações nos seguintes campos abaixo

   ```bash
    # database
    DATABASE_URL=

    # Postgis
    POSTGRES_USER=
    POSTGRES_DB=
    POSTGRES_PASSWORD=

    # openrouter
    OPEN_ROUTER_TOKEN=
   ```

   O **OPEN_ROUTER_TOKEN** é o token gerado dentro da conta no site do [Open Router Service](https://openrouteservice.org/)

   > [!NOTE]
   > O database url segue o padrão utilizado pelo sqlachelmy
   >
   > "postgresql+psycopg://user:password@host:port/database"

3. **Subir a aplicação**

   ```bash
   docker compose up -d
   ```

## Executar os teste

```bash
poetry shell
task test
```

### Parar o Container da aplicação

#### Parar aplicação

```bash
docker compose stop
```

#### Parar e remover o Container

```bash
docker compose down
```

> [!CAUTION]
> Ao parar o container da aplicação e remover o volume, irá apagar todos os dados salvos, faça isso somente se necessário.

```bash
docker compose down --volumes # or docker compose down -v
```

## Possíveis erros

- ### Falha na instalação do python
  
    Ao instalar o **python** pelo **pyenv** pode ocorrer uma falha por falta de dependências no sistema, para isso siga as instruções indicadas na wiki do pyenv.
    [WIKI - Suggested build environment](https://github.com/pyenv/pyenv/wiki)

## Referencias

- [Working with Spatial Data using FastAPI and GeoAlchemy](https://medium.com/@notarious2/working-with-spatial-data-using-fastapi-and-geoalchemy-797d414d2fe7) by Bekzod Mirahmedov
- [Which data type for latitude and longitude?](https://stackoverflow.com/questions/8150721/which-data-type-for-latitude-and-longitude)
- [GeoAlchemy2](https://geoalchemy-2.readthedocs.io/en/latest/search.html?q=geometry) by @[GeoAlchemy](https://github.com/geoalchemy)
- [FastAPI do Zero](https://fastapidozero.dunossauro.com/) by @[Dunossauro](https://github.com/dunossauro)
- [Pyenv](https://github.com/pyenv/pyenv)

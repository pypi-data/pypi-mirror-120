# Wrapper para trabalhar com a API do Cloud Logging

## Procedimento para upload no Pypi

### Pré requisitos
Instalar pacotes python
`python3 -m pip install --upgrade setuptools build wheel twine`

### Build e enviar ao PYPI

`python3 -m build`

`python3 -m twine upload dist/*`


### Instalar o pacote no projeto

`pip install fastapi-skywalking-trace`


## Utilização da biblioteca

Essa biblioteca espera que você passe o schema dos dados da tabela

Aconselho criar um arquivo de schema.py ou model.py onde seja definido a estrutura de dados da tabela.

### Instanciar o Middleware

Com o schema definido, você deve instanciar um classe

```python
from starlette.middleware import Middleware
from fastapi_skywalking_trace.middleware import SkywalkingMiddleware
middlewares = [
    Middleware(
        SkywalkingMiddleware,
        service_name='extractor',
        collector_address='35.266.138.244:15870',
        protocol = 'http'
    )
]

app = FastAPI(
    title='Iris Typification', 
    openapi_url="/api/v1/openapi.json",
    middleware=middlewares
    )

```

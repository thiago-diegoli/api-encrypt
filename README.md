# API Flask para Cifra de César

Uma API simples em Flask para login e criptografia usando a Cifra de César, desenvolvida para integrar com o aplicativo [CifraCesar](https://github.com/paulovictorio/CifraCesar).

## Pré-requisitos

- Python 3.x instalado
- Pip (gerenciador de pacotes do Python)

## Como configurar e executar

1. Clone o repositório ou baixe os arquivos da API

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Execute a aplicação:

```bash
python app.py
```

A API estará rodando em `http://localhost:5000` por padrão.

## Endpoints disponíveis

- `POST /login` - Autenticação de usuário
- `POST /encrypt` - Criptografa texto usando Cifra de César
- `POST /decrypt` - Descriptografa texto usando Cifra de César

## Configuração

Você pode alterar a porta padrão modificando a última linha do `app.py`:

```python
if __name__ == '__main__':
    app.run(port=5000)  # Altere o número da porta se necessário
```

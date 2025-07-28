# Instruções para uso do Alembic

## 1. Configuração inicial

- **Configurar o `alembic.ini`** com o driver do banco de dados que está sendo utilizado.

## 2. Inicializar o Alembic

> Essa etapa pode ser ignorada caso o projeto já esteja versionado com a pasta `alembic`.

```bash
alembic init alembic
```

## 3. Ajustar `env.py`

- No arquivo `alembic/env.py`, altere as configurações de **`metadata`** para apontar para as models do seu projeto.
- Essa configuração também já deve estar versionada no repositório.

> **Importante:** As models precisam estar disponíveis no `env.py` para que a geração automática de migrations funcione corretamente.

## 4. Criar uma nova migração

```bash
alembic revision --autogenerate -m "{revision_name}"
```

## 5. Aplicar as migrações

```bash
alembic upgrade head
```

## 6. Reverter migrações

```bash
alembic downgrade -{revision_amount}
```
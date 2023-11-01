# fastapi-sqlmodel-alembic

## Installing

### Use poetry
```bash
poetry install
```

### Use Anaconda
```bash
conda create --name fastapi-sqlmodel-alembic python=3.11
conda activate fastapi-sqlmodel-alembic

pip install -r requirements.txt
```

`vim migrations`

```bash
sqlalchemy.url = postgresql+asyncpg://postgres:postgres@localhost:5432/fastapi_sqlmodel_alembic
# Docker environment
sqlalchemy.url = postgresql+asyncpg://postgres:postgres@db_server:5432/fastapi_sqlmodel_alembic
```

## Usage

```bash
# 1. 构建（使用Dockerfile）全部服务
sudo docker-compose up -d --build
# or 只启动数据库
sudo docker-compose up -d --build db_server
# or 启动全部服务，以下 2 ~ 7 均在 Docker 环境执行
sudo docker-compose up -d --build

# 2. generate alembic.ini file 和 migration folder，注意 -t async 参数
alembic init -t async migrations
# or 在 Docker 中生成
sudo docker-compose exec web_server alembic init -t async migrations

# 3. 生成第一个迁移文件，位于 migrations/versions/xxx_init.py，此时数据库里会产生一张表 alembic_version，数据为空
alembic revision --autogenerate -m "init"
# or 在 Docker 里
sudo docker-compose exec web_server alembic revision --autogenerate -m "init"

# 4. Apply the migration，生成所有 app/models 里定义的表，并会向 alembic_version 表插入一条记录，即 migrations/xxx_init.py 的 xxx 部分
alembic upgrade head
# or 在 Docker 里
sudo docker-compose exec web_server alembic upgrade head

# NOTE: 5 和 6 不是必须的
# 5. 比如新增了一个 model 后，再创建一个 migration file
alembic revision --autogenerate -m "add year"
# or 在容器里
sudo docker-compose exec web_server alembic revision --autogenerate -m "add year"

# 6. Apply the migration
alembic upgrade head
# or 在 Docker 里
sudo docker-compose exec web_server alembic upgrade head

# 7. 启动服务
uvicorn app.main:app --reload --workers 1 --host 0.0.0.0 --port 8000

# 8. test endpoint，如果是通过 Docker 启动的，端口是 docker-compose.yml 里配置的 8004
curl -d '{"name":"Midnight Fit", "artist":"Mogwai", "year":"2021"}' -H "Content-Type: application/json" -X POST http://localhost:8000/songs | json_pp -json_opt pretty,canonical

# 9. open link in browser
http://localhost:8000/songs
```

## 如何新增依赖
### 使用 Poetry
```bash
poetry add alembic fastapi sqlmodel uvicorn asyncpg
```

### 使用 pip
```bash
pip install alembic fastapi sqlmodel uvicorn asyncpg
# 写入 requirements.txt
pip freeze > requirments.txt
```
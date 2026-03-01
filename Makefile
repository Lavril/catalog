install:
	@pip install -r requirements.txt

build:
	@docker compose build

up:
	docker compose up --build

stop:
	@docker compose stop

down:
	@docker compose down -v

init:
	@docker exec -it catalog_app alembic revision --autogenerate -m "init"

migrate:
	@docker exec -it catalog_app alembic upgrade head

seed:
	@docker exec -it catalog_app python -m app.seed_runner
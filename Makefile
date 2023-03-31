.PHONY: makemigrations migrate

makemigrations:
	alembic revision --autogenerate -m $(msg)

migrate:
	alembic upgrade head
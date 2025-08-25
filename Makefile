# Shadow Cauldron Makefile
# Hooks into the recursive make system

# Include the Python-specific makefile
include tools/makefiles/python.mk

# Project-specific targets
.PHONY: dev migrate upgrade

dev: install
	uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

migrate:
	uv run alembic upgrade head

revision:
	uv run alembic revision --autogenerate -m "$(MSG)"

downgrade:
	uv run alembic downgrade -1

# Database shortcuts
reset-db:
	rm -f shadow_cauldron.db
	uv run alembic upgrade head
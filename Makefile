.PHONY: fmt lint fix mypy test all

fmt:
	ruff format .

lint:
	ruff check .

fix:
	ruff check --fix .

mypy:
	mypy .

test:
	pytest test/ -v

all: fmt lint fix mypy test
PHONY: fmt, lint, fix, mypy, all

fmt:
	ruff format .

lint:
	ruff check .

fix:
	ruff check --fix .

mypy:
	mypy .

all:
	make fmt
	make lint
	make fix
	make mypy
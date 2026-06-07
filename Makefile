.PHONY: install dev lint format test cov docker run

install:
	pip install ".[transcription]"

dev:
	pip install -e ".[transcription,dev]"

lint:
	ruff check src tests
	mypy src

format:
	ruff format src tests
	ruff check --fix src tests

test:
	pytest

cov:
	pytest --cov=subsmith --cov-report=term-missing

docker:
	docker build -t subsmith:latest .

run:
	subsmith run $(VIDEO)

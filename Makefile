install:
	python3 -m venv .venv
	source .venv/bin/activate && pip install -e .

dev:
	source .venv/bin/activate && fastapi dev app/main.py

serve:
	python3 -m http.server 5173

test:
	pytest -v

format:
	source .venv/bin/activate && ruff format .

kill:
	kill -9 $(lsof -t -i:8000) || true
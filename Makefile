# Git workflow commands
.PHONY: wip
wip:
	git add .
	git commit -m "WIP: Work in progress"
	git push

# Install command
.PHONY: install
install:
	uv venv
	uv pip install -r pyproject.toml
	
# Build command
.PHONY: build
build:
	uv run build

# Deploy command
.PHONY: deploy
deploy:
	uv run deploy

# Test command
.PHONY: test
test:
	uv run pytest -v --log-cli-level=INFO

# Lint command
.PHONY: lint
lint:
	uv run ruff check 
	uv run ruff format --check

# Display all available commands
.PHONY: help
help:
	@echo "Available commands:"
	@echo "  wip     - Commit and push work in progress"
	@echo "  install - Install dependencies"
	@echo "  build   - Build the project"
	@echo "  deploy  - Deploy the project"
	@echo "  test    - Run tests"
	@echo "  lint    - Run linter"
	@echo "  help    - Display this help message"

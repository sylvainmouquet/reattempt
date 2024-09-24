# Git workflow commands
.PHONY: wip
wip:
	git add .
	git commit -m "WIP: Work in progress"
	git push

# Install command
.PHONY: install
install:
	uv install

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
	uv run pytest

# Lint command
.PHONY: lint
lint:
	uv run lint

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

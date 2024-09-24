# Git workflow commands
.PHONY: wip
wip:
	git add .
	git commit -m "WIP: Work in progress"
	git push

# Install command
.PHONY: install
install:
	uv sync --all-extras --dev
	
# Build command
.PHONY: build
build: check-version
	rm -rf dist/* || true
#	ls -al
	$(sed -i 's/^version =.*/version = "${VERSION}"/' pyproject.toml)
	$(sed -i 's/^__version__ =.*/__version__ = "${VERSION}"/' src/reattempt/__init__.py)
	cat pyproject.toml | grep version
#	@sed -i '' 's/^version =.*/version = "${VERSION}"/' pyproject.toml
	uv build

.PHONY: check-version
check-version:
	@if [ -z "${VERSION}" ]; then \
		echo "VERSION is not set. Please set the VERSION environment variable."; \
		exit 1; \
	fi

# Deploy command
.PHONY: deploy
deploy:
	uvx twine upload dist/*

# Install local build command
.PHONY: install-local
install-local:
	pip3 install dist/*.whl

# Test command
.PHONY: test
test:
	uv run pytest -v --log-cli-level=INFO

# Lint command
.PHONY: lint
lint:
	uv run ruff check 
	uv run ruff format
	uv run ruff format --check

# Display all available commands
.PHONY: help
help:
	@echo "Available commands:"
	@echo "  wip           - Commit and push work in progress"
	@echo "  install       - Install dependencies"
	@echo "  build         - Build the project"
	@echo "  deploy        - Deploy the project"
	@echo "  install-local - Install the build locally"
	@echo "  test          - Run tests"
	@echo "  lint          - Run linter"
	@echo "  help          - Display this help message"

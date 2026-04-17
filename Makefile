# Package name, read from pyproject.toml so this Makefile is reusable across projects
PACKAGE := $(shell awk -F'"' '/^name = / {print $$2; exit}' pyproject.toml)

# Minimum coverage percentage required for tests to pass
COVERAGE_FAIL = 60

# Run the test suite
test:
	poetry run pytest

# Format the code using Ruff
format:
	poetry run ruff format .

# Lint the code using Ruff (configured in pyproject.toml [tool.ruff])
lint:
	poetry run ruff check .

# Run all quality checks: formatting, linting, and tests
check: format lint test

# Run tests with coverage enforcement (terminal output only)
# Omit patterns are configured in pyproject.toml [tool.coverage.run].
coverage:
	poetry run coverage run --source=$(PACKAGE) -m pytest
	poetry run coverage report --fail-under=$(COVERAGE_FAIL)

# Run tests with coverage and produce an HTML report
coverage-html:
	poetry run coverage run --source=$(PACKAGE) -m pytest
	poetry run coverage report --fail-under=$(COVERAGE_FAIL)
	poetry run coverage html
	@echo "HTML coverage report generated at htmlcov/index.html"

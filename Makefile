PIP = pip3
TEST_DIR = tests
PRJ = dial

.PHONY: test
test:
	pytest $(TEST_DIR)

.PHONY: cover
cover:
	pytest --cov=$(PRJ) $(TEST_DIR)

.PHONY: lint
lint:
	pylama

.PHONY: env
env:
	$(PIP) install -r requirements-dev.txt
	$(PIP) install -e .

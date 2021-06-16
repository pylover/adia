PIP = pip3
TEST_DIR = tests

.PHONY: test
test:
	pytest $(TEST_DIR)

.PHONY: cover
cover:
	pytest --cov=dial $(TEST_DIR)

.PHONY: env
env:
	$(PIP) install -r requirements-dev.txt
	$(PIP) install -e .

PIP = pip3

.PHONY: test
test:
	pytest

.PHONY: env
env:
	$(PIP) install -r requirements-dev.txt
	$(PIP) install -e .

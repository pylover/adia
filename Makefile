PIP = pip3
TEST_DIR = tests
PRJ = dial
PYTEST_FLAGS = -v


.PHONY: test
test:
	pytest $(PYTEST_FLAGS) $(TEST_DIR)

.PHONY: cover
cover:
	pytest $(PYTEST_FLAGS) --cov=$(PRJ) $(TEST_DIR)

.PHONY: lint
lint:
	pylama

.PHONY: env
env:
	$(PIP) install -r requirements-dev.txt
	$(PIP) install -e .


# WWW

WWW = www
WWWDIST = $(shell readlink -f $(WWW)/build)
DIAL = dial

$(WWWDIST)/dial.js:
	brython pack \
		--package-directory $(DIAL) \
		--output-directory $(WWWDIST) \
		dial
	
$(WWWDIST)/stdlib.min.js:
	- mkdir -p $(WWWDIST)
	brython pack-dependencies \
		--output-directory $(WWWDIST) \
		--search-directory $(DIAL) \
		--stdlib-directory $(WWW) \
		--filename stdlib.min.js

$(WWWDIST)/stdlib.full.js:
	- ln -s $(shell readlink -f $(WWW))/stdlib.full.js $(WWWDIST)

$(WWWDIST)/runtime.js:
	- ln -s $(shell readlink -f $(WWW))/brython.js $(WWWDIST)/runtime.js

$(WWWDIST)/index.html:
	- ln -s $(shell readlink -f $(WWW))/index.html $(WWWDIST)

$(WWWDIST)/check.html:
	- ln -s $(shell readlink -f $(WWW))/check.html $(WWWDIST)

$(WWWDIST)/check.py:
	- ln -s $(shell readlink -f $(WWW))/check.py $(WWWDIST)

$(WWWDIST)/kitchen.html:
	- ln -s $(shell readlink -f $(WWW))/kitchen.html $(WWWDIST)

$(WWWDIST)/kitchen.py:
	- ln -s $(shell readlink -f $(WWW))/kitchen.py $(WWWDIST)

$(WWWDIST)/favicon.ico:
	- ln -s $(shell readlink -f $(WWW))/favicon.ico $(WWWDIST)

$(WWWDIST)/tests:
	- ln -s $(shell readlink -f tests) $(WWWDIST)

.PHONY: www
www: \
	$(WWWDIST)/stdlib.full.js \
	$(WWWDIST)/stdlib.min.js \
	$(WWWDIST)/dial.js \
	$(WWWDIST)/index.html \
	$(WWWDIST)/check.html \
	$(WWWDIST)/check.py \
	$(WWWDIST)/tests \
	$(WWWDIST)/kitchen.py \
	$(WWWDIST)/kitchen.html \
	$(WWWDIST)/favicon.ico \
	$(WWWDIST)/runtime.js

.PHONY: serve
serve: www
	brython -C$(WWWDIST) serve --port 8000

.PHONY: update-brython.js
update-brython.js: www
	cp ../brython/www/src/brython.js $(WWW)
	cp ../brython/www/src/brython_stdlib.js $(WWW)

.PHONY: clear
clean::
	- rm -rf $(DIAL)/__pycache__
	- rm \
		$(WWWDIST)/runtime.js \
		$(WWWDIST)/stdlib.*.js \
		$(WWWDIST)/dial.js \
		$(WWWDIST)/tests \
		$(WWWDIST)/check.py \
		$(WWWDIST)/check.html \
		$(WWWDIST)/kitchen.py \
		$(WWWDIST)/kitchen.html \
		$(WWWDIST)/favicon.ico \
		$(WWWDIST)/index.html

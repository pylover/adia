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
WWWDIST = $(WWW)/build
WWWDIST_ABS = $(shell readlink -f $(WWWDIST))
DIAL = dial

$(WWWDIST)/dial.js:
	brython pack \
		--package-directory $(DIAL) \
		--output-directory $(WWWDIST) \
		dial
	
$(WWWDIST)/stdlib.js: $(WWWDIST)/brython_stdlib.js
	- mkdir -p $(WWWDIST)
	brython pack-dependencies \
		--output-directory $(WWWDIST) \
		--search-directory $(DIAL) \
		--stdlib-directory $(WWWDIST) \
		--filename stdlib.js

$(WWWDIST)/index.html:
	- ln -s $(shell readlink -f $(WWW))/index.html $(WWWDIST_ABS)

$(WWWDIST)/check.html:
	- ln -s $(shell readlink -f $(WWW))/check.html $(WWWDIST_ABS)

$(WWWDIST)/check.py:
	- ln -s $(shell readlink -f $(WWW))/check.py $(WWWDIST_ABS)

$(WWWDIST)/kitchen.html:
	- ln -s $(shell readlink -f $(WWW))/kitchen.html $(WWWDIST_ABS)

$(WWWDIST)/kitchen.py:
	- ln -s $(shell readlink -f $(WWW))/kitchen.py $(WWWDIST_ABS)

$(WWWDIST)/favicon.ico:
	- ln -s $(shell readlink -f $(WWW))/favicon.ico $(WWWDIST_ABS)

$(WWWDIST)/tests:
	- ln -s $(shell readlink -f tests) $(WWWDIST_ABS)

.PHONY: www
www: \
	$(WWWDIST)/brython.js \
	$(WWWDIST)/brython_stdlib.js \
	$(WWWDIST)/stdlib.js \
	$(WWWDIST)/dial.js \
	$(WWWDIST)/index.html \
	$(WWWDIST)/check.html \
	$(WWWDIST)/check.py \
	$(WWWDIST)/tests \
	$(WWWDIST)/kitchen.py \
	$(WWWDIST)/kitchen.html \
	$(WWWDIST)/favicon.ico

.PHONY: serve
serve: www
	brython -C$(WWWDIST) serve --port 8000

BRYTHON_REPO = https://raw.githubusercontent.com/brython-dev/brython
BRYTHON_URL = $(BRYTHON_REPO)/master/www/src

$(WWWDIST)/%.js:
	curl "$(BRYTHON_URL)/$(shell basename $@)" > $@

.PHONY: clean
clean:
	- rm -rf $(DIAL)/__pycache__
	- rm \
		$(WWWDIST)/stdlib.js \
		$(WWWDIST)/dial.js \
		$(WWWDIST)/tests \
		$(WWWDIST)/check.py \
		$(WWWDIST)/check.html \
		$(WWWDIST)/kitchen.py \
		$(WWWDIST)/kitchen.html \
		$(WWWDIST)/favicon.ico \
		$(WWWDIST)/index.html

.PHONY: cleanall
cleanall: clean
	- rm \
		$(WWWDIST)/brython_stdlib.js \
		$(WWWDIST)/brython.js \

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
BRYTHON_REPO = https://raw.githubusercontent.com/brython-dev/brython
BRYTHON_URL = $(BRYTHON_REPO)/master/www/src
BRYTHON_FILES = \
	$(WWWDIST)/brython.js \
	$(WWWDIST)/brython_stdlib.js

DIST_FILES = \
	$(WWWDIST)/index.html \
	$(WWWDIST)/check.html \
	$(WWWDIST)/check.py \
	$(WWWDIST)/kitchen.py \
	$(WWWDIST)/kitchen.html \
	$(WWWDIST)/favicon.ico

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

$(WWWDIST)/tests:
	- ln -s $(shell readlink -f tests) $(WWWDIST_ABS)

$(BRYTHON_FILES): $(WWWDIST)/%.js:
	curl "$(BRYTHON_URL)/$(shell basename $@)" > $@

$(DIST_FILES): $(WWWDIST)/%:
	ln -s $(shell readlink -f $(WWW)/$(shell basename $@)) $(WWWDIST_ABS)

.PHONY: www
www: $(DIST_FILES) $(BRYTHON_FILES) $(WWWDIST)/dial.js $(WWWDIST)/tests \
	$(WWWDIST)/stdlib.js

.PHONY: serve
serve: www
	brython -C$(WWWDIST) serve --port 8000


.PHONY: clean
clean:
	- rm -rf $(DIAL)/__pycache__
	- rm $(DIST_FILES)
	- rm $(WWWDIST)/tests
	- rm $(WWWDIST)/stdlib.js
	- rm $(WWWDIST)/dial.js

.PHONY: cleanall
cleanall: clean
	- rm $(BRYTHON_FILES)

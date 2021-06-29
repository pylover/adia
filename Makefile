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
	- cp $(WWW)/brython_stdlib.js $(WWWDIST)/stdlib.full.js

$(WWWDIST)/index.html:
	- ln -s $(shell readlink -f $(WWW))/index.html $(WWWDIST)

$(WWWDIST)/test.html:
	- ln -s $(shell readlink -f $(WWW))/test.html $(WWWDIST)

$(WWWDIST)/kitchen.html:
	- ln -s $(shell readlink -f $(WWW))/kitchen.html $(WWWDIST)

$(WWWDIST)/webtests.py:
	- ln -s $(shell readlink -f $(WWW))/webtests.py $(WWWDIST)

$(WWWDIST)/kitchen.py:
	- ln -s $(shell readlink -f $(WWW))/kitchen.py $(WWWDIST)

$(WWWDIST)/tests:
	- ln -s $(shell readlink -f tests) $(WWWDIST)

.PHONY: www
www: $(WWWDIST)/stdlib.full.js $(WWWDIST)/stdlib.min.js $(WWWDIST)/dial.js \
	$(WWWDIST)/index.html $(WWWDIST)/test.html $(WWWDIST)/webtests.py \
	$(WWWDIST)/tests $(WWWDIST)/kitchen.py $(WWWDIST)/kitchen.html
	- cp $(WWW)/brython.js $(WWWDIST)/runtime.js

.PHONY: serve
serve: www
	brython -C$(WWWDIST) serve --port 9001

.PHONY: clear
clean::
	- rm -rf $(DIAL)/__pycache__
	- rm \
		$(WWWDIST)/runtime.js \
		$(WWWDIST)/stdlib.*.js \
		$(WWWDIST)/dial.js \
		$(WWWDIST)/tests \
		$(WWWDIST)/webtests.py \
		$(WWWDIST)/test.html \
		$(WWWDIST)/kitchen.py \
		$(WWWDIST)/kitchen.html \
		$(WWWDIST)/index.html

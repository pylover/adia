PIP = pip3
TEST_DIR = tests
PRJ = adia
PYTEST_FLAGS = -v
ADIA_VER = $(shell adia --version | cut -d'.' -f1-2)
SPHINX_BUILDDIR = documentation/_build
JSDIST = build/jsdist
JSDISTVER = "$(JSDIST)/$(ADIA_VER)"

.PHONY: test
test:
	pytest $(PYTEST_FLAGS) $(TEST_DIR)

.PHONY: cover
cover:
	pytest $(PYTEST_FLAGS) --cov=$(PRJ) $(TEST_DIR)

.PHONY: lint
lint:
	flake8

.PHONY: env
env:
	$(PIP) install -r requirements-dev.txt
	$(PIP) install -e .


.PHONY: sdist
sdist:
	python3 setup.py sdist

.PHONY: bdist
bdist:
	python3 setup.py bdist_egg


.PHONY: dist
dist: sdist bdist

.PHONY: pypi
pypi: dist
	twine upload dist/*.gz dist/*.egg

.PHONY: doc
doc:
	cd documentation; make clean html
	ln -sf $(ADIA_VER) "$(SPHINX_BUILDDIR)/latest"

.PHONY: livedoc
livedoc:
	cd documentation; make clean livehtml

.PHONY: doctest
doctest:
	cd documentation; make doctest


# WEBCLINIC
WEBCLINIC = webclinic
WEBCLINIC_BUILD = $(WEBCLINIC)/build
WEBCLINIC_BUILD_ABS = $(shell readlink -f $(WEBCLINIC_BUILD))
ADIA = adia
BRYTHON_REPO = https://raw.githubusercontent.com/brython-dev/brython
BRYTHON_URL = $(BRYTHON_REPO)/master/www/src
BRYTHON_FILES = \
	$(WEBCLINIC_BUILD)/brython.js \
	$(WEBCLINIC_BUILD)/brython_stdlib.js

DIST_FILES = \
	$(WEBCLINIC_BUILD)/index.html \
	$(WEBCLINIC_BUILD)/check.html \
	$(WEBCLINIC_BUILD)/check.py \
	$(WEBCLINIC_BUILD)/adia_worker.py \
	$(WEBCLINIC_BUILD)/adia.js \
	$(WEBCLINIC_BUILD)/global.css \
	$(WEBCLINIC_BUILD)/favicon.ico

# Not neede anymore after v2.
$(WEBCLINIC_BUILD)/adia.brython.js:
	- mkdir -p $(WEBCLINIC_BUILD)
	brython pack \
		--package-directory $(ADIA) \
		--output-directory $(WEBCLINIC_BUILD) \
		adia

$(WEBCLINIC_BUILD)/adia:
	ln -s $(shell readlink -f adia) $(WEBCLINIC_BUILD)

$(WEBCLINIC_BUILD)/adia.stdlib.js: \
		$(WEBCLINIC_BUILD)/brython_stdlib.js \
		$(WEBCLINIC_BUILD)/adia \
		$(WEBCLINIC_BUILD)/adia_worker.py
	- mkdir -p $(WEBCLINIC_BUILD)
	brython pack-dependencies \
		--output-directory $(WEBCLINIC_BUILD) \
		--search-directory $(WEBCLINIC) \
		--stdlib-directory $(WEBCLINIC_BUILD) \
		--exclude check* \
		--exclude test/* \
		--filename adia.stdlib.js

$(WEBCLINIC_BUILD)/tests:
	- mkdir -p $(WEBCLINIC_BUILD)
	ln -s $(shell readlink -f tests) $(WEBCLINIC_BUILD_ABS)

$(BRYTHON_FILES): $(WEBCLINIC_BUILD)/%.js:
	- mkdir -p $(WEBCLINIC_BUILD)
	curl "$(BRYTHON_URL)/$(shell basename $@)" > $@

$(DIST_FILES): $(WEBCLINIC_BUILD)/%:
	- mkdir -p $(WEBCLINIC_BUILD)
	ln -s $(shell readlink -f $(WEBCLINIC)/$(shell basename $@)) \
		$(WEBCLINIC_BUILD_ABS)

$(WEBCLINIC_BUILD)/adia.bundle.js: $(BRYTHON_FILES) \
		$(WEBCLINIC_BUILD)/adia.js $(WEBCLINIC_BUILD)/adia.stdlib.js
	cat $(WEBCLINIC_BUILD)/brython.js > $@
	echo >> $@
	cat $(WEBCLINIC_BUILD)/adia.stdlib.js >> $@
	echo >> $@
	cat $(WEBCLINIC_BUILD)/adia.js >> $@
	echo >> $@


.PHONY: jsdist
jsdist: $(WEBCLINIC_BUILD)/adia.bundle.js $(WEBCLINIC_BUILD)/adia.js
	-rm -rf $(JSDISTVER)
	mkdir -p $(JSDISTVER)
	cp $(WEBCLINIC_BUILD)/adia.bundle.js $(JSDISTVER)/adia.bundle.js
	cp $(WEBCLINIC_BUILD)/adia.stdlib.js $(JSDISTVER)/adia.stdlib.js
	cp $(WEBCLINIC_BUILD)/adia.js $(JSDISTVER)/adia.js
	cp $(WEBCLINIC_BUILD)/adia_worker.py $(JSDISTVER)/adia_worker.py
	cp -r $(ADIA) $(JSDISTVER)
	rm -rf $(JSDISTVER)/adia/__pycache__
	cd $(JSDISTVER); tar -cvzf ../adia-$(ADIA_VER).tar.gz ./*

.PHONY: webclinic
webclinic: \
		$(DIST_FILES) \
		$(WEBCLINIC_BUILD)/adia.bundle.js \
		$(WEBCLINIC_BUILD)/tests 


.PHONY: serve
webclinic_serve: webclinic
	brython -C$(WEBCLINIC_BUILD) serve --port 8000


.PHONY: clean
clean:
	- rm -rf $(ADIA)/__pycache__
	- rm $(DIST_FILES)
	- rm -rf $(JSDIST)/*
	- rm $(WEBCLINIC_BUILD)/tests
	- rm $(WEBCLINIC_BUILD)/adia.stdlib.js
	- rm $(WEBCLINIC_BUILD)/adia.brython.js
	- rm $(WEBCLINIC_BUILD)/adia.bundle.js
	- rm $(WEBCLINIC_BUILD)/adia
	- rm dist/*.egg
	- rm dist/*.gz

.PHONY: cleanall
cleanall: clean
	- rm $(BRYTHON_FILES)

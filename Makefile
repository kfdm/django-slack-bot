PYTHON_BIN := .venv/bin/python
PIP_BIN := .venv/bin/pip

.PHONY: build
build: $(PYTHON_BIN)
	$(PYTHON_BIN) setup.py sdist bdist_wheel

$(PYTHON_BIN):
	python3 -m venv .venv
	$(PIP_BIN) install wheel

.PHONY:	check
check:
	twine check dist/*.tar.gz

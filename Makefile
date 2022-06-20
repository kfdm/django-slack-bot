PYTHON_BIN := .venv/bin/python
PIP_BIN := .venv/bin/pip
APP_BIN := .venv/bin/example-bot

.PHONY: test
test: $(APP_BIN)
	$(APP_BIN) test

$(APP_BIN): $(PYTHON_BIN)
	$(PIP_BIN) install -e .[example]

.PHONY: build
build: $(PYTHON_BIN)
	git clean -dxf build
	$(PYTHON_BIN) setup.py sdist bdist_wheel

$(PYTHON_BIN):
	python3 -m venv .venv
	$(PIP_BIN) install wheel

.PHONY:	check
check:
	twine check dist/*.tar.gz

.PHONY: clean
clean:
	git clean -dxf dist build

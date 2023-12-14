ENV_DIR := .venv
APP_BIN := $(ENV_DIR)/bin/django-admin
PIP_BIN := $(ENV_DIR)/bin/pip
PYTHON_BIN := $(ENV_DIR)/bin/python
TWINE_BIN := $(ENV_DIR)/bin/twine
PKG_DIR := dsbot
SYSTEM_PYTHON := python3.9

.PHONY:	test build check clean
.DEFAULT: test

test: ${APP_BIN}
	${PYTHON_BIN} -m tests.example -v 2

$(PIP_BIN):
	$(SYSTEM_PYTHON) -m venv .venv

${APP_BIN}: $(PIP_BIN)
	${PIP_BIN} install -e .

${TWINE_BIN}: $(PIP_BIN)
	$(PIP_BIN) install wheel twine build

.PHONY: build
build: $(TWINE_BIN)
	$(PYTHON_BIN) -m build
	$(TWINE_BIN) check dist/*

clean:
	rm -rf .venv dist

.PHONY: changelog
changelog:
	git log --color=always --first-parent --pretty='format:%s|%Cgreen%d%Creset'  | column -ts '|'

###############################################################################
### Formatting
###############################################################################
RUFF_BIN := $(ENV_DIR)/bin/ruff

$(RUFF_BIN): $(PIP_BIN)
	$(PIP_BIN) install ruff

.PHONY: format
format: $(RUFF_BIN)
	$(RUFF_BIN) check --fix $(PKG_DIR)
	$(RUFF_BIN) format $(PKG_DIR)

.PHONY: check
check: $(RUFF_BIN)
	$(RUFF_BIN) check $(PKG_DIR)
	$(RUFF_BIN) format --check $(PKG_DIR)

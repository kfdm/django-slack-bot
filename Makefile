PYTHON_BIN := .venv/bin/python

.PHONY: build
build: .venv
	$(PYTHON_BIN) setup.py sdist

.venv:
	python3 -m venv .venv

.PHONY:	check
check:
	twine check dist/*.tar.gz

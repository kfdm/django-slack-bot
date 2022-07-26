APP_BIN := .venv/bin/django-admin
PIP_BIN := .venv/bin/pip
PYTHON_BIN := .venv/bin/python
TWINE_BIN := .venv/bin/twine

.PHONY:	test build check clean
.DEFAULT: test

test: ${APP_BIN}
	${PYTHON_BIN} -m tests.example -v 2

$(PIP_BIN):
	python3 -m venv .venv

${APP_BIN}: $(PIP_BIN)
	${PIP_BIN} install -e .

${TWINE_BIN}: $(PIP_BIN)
	$(PIP_BIN) install wheel twine

.PHONY: build
build: $(TWINE_BIN)
	$(PYTHON_BIN) setup.py sdist bdist_wheel
	$(TWINE_BIN) check dist/*

clean:
	rm -rf .venv dist

.PHONY: changelog
changelog:
	git log --color=always --first-parent --pretty='format:%s|%Cgreen%d%Creset'  | column -ts '|'

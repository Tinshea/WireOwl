OS := $(shell uname | tr '[:upper:]' '[:lower:]')
IS_WINDOWS := $(findstring mingw,$(OS))

ifeq ($(IS_WINDOWS),mingw)
ACTIVATE = .venv/Scripts/activate
PYTHON = python
else
ACTIVATE = .venv/bin/activate
PYTHON = python3
endif

run:
	. $(ACTIVATE) && $(PYTHON) core/main.py

setup:
	$(PYTHON) -m venv .venv && . $(ACTIVATE) && pip install -r Tools/requirements.txt

clean:
	rm -rf core/__pycache__

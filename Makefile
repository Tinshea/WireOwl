run:
	. .venv/bin/activate && python3 core/main.py
setup:
	python3 -m venv .venv && . .venv/bin/activate && pip install -r Tools/requirements.txt 
clean:
	rm  -rf core/__pycache__ 

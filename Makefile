run:
	uvicorn app.main:app --reload

venv:
	source venv/bin/activate

install:
	make venv
	pip install -r requirements.txt

save:
	make venv
	pip freeze > requirements.txt

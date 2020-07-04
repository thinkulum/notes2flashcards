.PHONY: clean virtualenv test docker dist dist-upload

clean:
	find . -name '*.py[co]' -delete

virtualenv:
	virtualenv --prompt '|> notes2flashcards <| ' env
	env/Scripts/pip install -r requirements-dev.txt
	env/Scripts/python setup.py develop
	@echo
	@echo "VirtualENV Setup Complete. Now run: source env/Scripts/activate"
	@echo

test:
	python -m pytest \
		-v \
		--cov=notes2flashcards \
		--cov-report=term \
		--cov-report=html:coverage-report \
		tests/

docker: clean
	docker build -t notes2flashcards:latest .

dist: clean
	rm -rf dist/*
	python setup.py sdist
	python setup.py bdist_wheel

dist-upload:
	twine upload dist/*

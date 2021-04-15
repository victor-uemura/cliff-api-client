PYLINT := env PYTHONPATH=$(PYTHONPATH) pylint

install:
	pip install -r requirements.txt

lint:
	$(PYLINT) cliff

test:
	python3 setup.py test

build-release:
	find . -name '.DS_Store' -type f -delete
	python3 setup.py sdist

release-test:
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

release:
	twine upload dist/*

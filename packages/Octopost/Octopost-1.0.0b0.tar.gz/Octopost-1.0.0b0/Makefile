.PHONY: build
.PHONY: test
.PHONY: doc

install:
	pip install .

install-test:
	pip install -e .[test]

install-dev:
	pip install -e .[test,dev]

build:
	python setup.py sdist bdist_wheel

clean_small:
	rm -fr build/
	rm -fr .eggs/
	rm -fr .tox/
	rm -fr .pytest_cache
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean:
	make clean_small
	rm -fr lint.log
	rm -fr tox.log
	rm -fr ./dist
	rm -fr docs/_build

test:
	pytest
	for file in `ls demo/scripts` ; do \
		echo $$file ; \
		python demo/scripts/$$file ; \
	done
	

html:
	make -C docs html

lint:
	flake8 ./src --ignore=W605,W504

prepare:
	make clean
	make install-dev
	make lint
	make test
	make html
	make build
	make clean_small

publish:
	twine upload dist/*

.PHONY: all test flake8

all: test flake8

flake8:
	python -m flake8 ./lazy_ips

test:
	python -m pytest ./tests

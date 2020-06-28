current_dir = $(shell pwd)

install:
	@pip install coverage

unit-test:
	@python -m unittest discover -s $(current_dir) -p '*_test.py'

unit-test-coverage:
	@coverage run -m unittest discover -s $(current_dir) -p '*_test.py'
	@coverage html

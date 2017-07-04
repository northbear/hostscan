

.PHONY: clean test

clean:
	@rm *.pyc

test:
	python -m unittest discover -s tests

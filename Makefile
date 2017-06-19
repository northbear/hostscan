

.PHONY: clean test

clean:
	@if [ -f *.pyc ]; then rm *.pyc; fi

test:
	python -m unittest discover -s tests

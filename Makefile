

publish:
	python3 setup.py sdist bdist_wheel
	twine check dist/*
	twine upload dist/*

clean:
	rm -Rf build dist *.egg-info

test-type:
	python3 -m mypy --strict py_matching_pattern

test: test-type
	python3 -m unittest --failfast tests/test_core.py

test-single:
	python3 -m unittest --failfast $(TEST)
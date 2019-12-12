

publish:
	python3 setup.py sdist bdist_wheel
	twine check dist/*
	twine upload dist/*

clean:
	rm -Rf build dist *.egg-info

test:
	python3 -m unittest --failfast tests/test_core.py

test-single:
	python3 -m unittest --failfast $(TEST)
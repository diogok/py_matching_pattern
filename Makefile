

publish:
	python3 setup.py sdist bdist_wheel
	twine check dist/*
	twine upload dist/*

clean:
	rm -Rf build dist *.egg-info

test:
	python3 -m unittest tests/test_core.py
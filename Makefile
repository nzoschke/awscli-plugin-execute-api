upload:
	python3 -m pip install --user --upgrade setuptools twine wheel
	python3 setup.py sdist bdist_wheel
	twine upload dist/*


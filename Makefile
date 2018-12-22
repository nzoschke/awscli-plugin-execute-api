clean:
	rm -f awscli_plugin_execute_api.egg-info
	rm -f build
	rm -f dist

upload:
	python3 -m pip install --user --upgrade setuptools twine wheel
	python3 setup.py sdist bdist_wheel
	twine upload dist/*



default:
	@echo "\"make upload\"?"

README.rst: README.md
	pandoc README.md -o README.rst

upload: setup.py README.rst
	python setup.py sdist upload --sign

clean:
	rm -f README.rst

test:
	pytest

doc:
	cd docs; $(MAKE) html

clean:
	cd docs; $(MAKE) clean

build:
	python3 setup.py sdist bdist_wheel
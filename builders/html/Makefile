pre-build:
	rm -rf build
	mkdir build
	cp -r template/assets build/

build: pre-build
	python3.10 build.py $(SOURCE)

preview:
	python3.10 preview.py $(SOURCE)


.PHONY: pre-build build preview

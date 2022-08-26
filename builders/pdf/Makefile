pre-build:
	rm -rf build
	mkdir build
	cp template/jameel-noori-nastaleeq.ttf build/

build: pre-build
	python3.10 build.py $(SOURCE)
	cd build; xelatex story.tex

preview: build
	python3.10 -m http.server -d build


.PHONY: build pre-build preview

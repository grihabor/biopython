DOC_IMAGE=doc_image


all: bash

bash: build
	docker run -it \
		-v $(shell pwd)/..:/documents \
		$(DOC_IMAGE)

build:
	docker build . -t $(DOC_IMAGE)

convert:
	python3 convert.py ..

.PHONY: all build bash convert

FILE=Tutorial
FILE_TEX=$(FILE).tex
FILE_RST=$(FILE).rst
DOC_IMAGE=doc_image


all: bash

bash: build
	docker run -it \
		-v $(shell pwd)/..:/documents \
		$(DOC_IMAGE)

build:
	docker build . -t $(DOC_IMAGE)

.PHONY: all build bash

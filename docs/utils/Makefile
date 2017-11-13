DOC_IMAGE=grihabor/sphinx
DOC_DIR=$(shell pwd)

all: bash

bash: pull
	docker run -it \
		-v $(DOC_DIR)/..:/documents \
		$(DOC_IMAGE)

pull:
	docker pull $(DOC_IMAGE)

convert:
	python3 convert.py ..

docs:
	docker run -it \
		-v $(DOC_DIR)/..:/documents \
		$(DOC_IMAGE) \
		python3 $(DOC_DIR)/

.PHONY: all bash pull convert

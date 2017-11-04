FILE=Tutorial
FILE_TEX=$(FILE).tex
FILE_RST=$(FILE).rst
DOC_IMAGE=doc_image


all:
	pandoc --from=latex --to=rst $(FILE_TEX) > $(FILE_RST)

bash: build
	docker run -it \
		-v $(shell pwd)/..:/documents \
		$(DOC_IMAGE)

build:
	docker build . -t $(DOC_IMAGE)

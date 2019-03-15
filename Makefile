all: update deploy

.PHONY: deploy
deploy:
	STATIC_DEPS=true pip3 install -U twitter -t .
	serverless deploy

.PHONY: update
update:
	python scrape_xml.py

.PHONY: clean
clean:
	git clean -fd


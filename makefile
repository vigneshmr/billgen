.DEFAULT_GOAL := bill

env:
	virtualenv env
	$@/bin/pip install -r requirements.txt

bill: | env
	$|/bin/python bill_gen.py

.PHONY: nuke
nuke:
	rm -rf env

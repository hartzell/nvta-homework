SHELL:=/usr/bin/env bash

.PHONY: lint
lint:
	# mypy nvta_homework tests/**/*.py
	flake8 --config=setup.cfg .
	yapf -d -r nvta-homework tests docs
	doc8 -q docs

.PHONY: unit
unit:
	pytest

.PHONY: package
package:
	poetry check
	pip check
	safety check --bare --full-report

.PHONY: test
test: lint unit package

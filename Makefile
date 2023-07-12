SHELL=/bin/bash


# List of all targets that are not files
.PHONY: git  test style


test:
	@pytest tests/ -s

style: 
	@black easy_ge/
	@isort easy_ge/
	@pylint --recursive=y -sn -rn easy_ge/ --ignore-imports=yes  --errors-only --exit-zero

git: 
	@git add . && git commit -m "$$(openssl rand -hex 5)" && git push -u origin main

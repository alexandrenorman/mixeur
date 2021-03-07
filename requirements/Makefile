upgrade:
	pip-compile --annotate -U base.in -v -o  base.txt
	pip-compile --annotate -U production.in -v -o  production.txt
	pip-compile --annotate -U development.in -v -o  development.txt

cache:
	mkdir -p ../../.cache
	cd ../../.cache ; pip --cache-dir . download -r ../django/requirements/development.txt
	cd ../../.cache ; pip --cache-dir . download -r ../django/requirements/production.txt

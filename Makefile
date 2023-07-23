.PHONY: dependencies
pip-install:
	pip install -r requirements.txt


.PHONY: docker
start-docker:
	docker-compose up -d

.PHONY: python_scripts
perform-etl:
	python main.py --endpoint-url http://localhost:4566 --queue-name login-queue --max-messages 10

run:
	uvicorn app.main:app --reload

venv:
	source venv/bin/activate

install:
	make venv
	pip install -r requirements.txt

save:
	make venv
	pip freeze > requirements.txt

deploy:
	docker buildx build --platform=linux/amd64 --no-cache -t upload-image .
	aws ecr get-login-password --region ap-northeast-2 --profile soma-wonyang | docker login --username AWS --password-stdin 975049979695.dkr.ecr.ap-northeast-2.amazonaws.com/flash/service_dev
	docker tag upload-image:latest 975049979695.dkr.ecr.ap-northeast-2.amazonaws.com/flash/service_dev:latest
	docker push 975049979695.dkr.ecr.ap-northeast-2.amazonaws.com/flash/service_dev:latest

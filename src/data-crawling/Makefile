AWS_CURRENT_REGION_ID := $(shell aws configure get region)
AWS_CURRENT_ACCOUNT_ID := $(shell aws sts get-caller-identity --query "Account" --output text)
IMAGE_TAG := "latest"

help:
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

local-build: # Build lambda crawler on local.
	docker buildx build --platform linux/amd64 -t crawler .

local-deploy: # Deploy lambda crawler custom docker image on local.
	docker run \
		-p 9000:8080 \
		--network twinllm_my_network \
		--platform linux/amd64 \
		crawler:latest

local-test: # Send test command on local to test  the lambda
	curl -X POST "http://localhost:9000/2015-03-31/functions/function/invocations" \
	  	-d '{"user": "Paul Iuztin", "link": "https://edition.cnn.com/2024/07/09/politics/joshua-kindred-resignation/index.html"}'

invoke: # Invoke remote lambda from local
	aws lambda invoke \
		--function-name crawler \
		--cli-binary-format raw-in-base64-out \
		--payload '{"user": "Paul Iuztin", "link": "https://medium.com/@pauliusztin/the-llms-kit-build-a-production-ready-real-time-financial-advisor-system-using-streaming-ffdcb2b50714"}' \
		response.json

push: # Build & push image to docker ECR (e.g make push IMAGE_TAG=latest)
	echo "Logging into AWS ECR..."
	aws ecr get-login-password --region $(AWS_CURRENT_REGION_ID) | docker login --username AWS --password-stdin $(AWS_CURRENT_ACCOUNT_ID).dkr.ecr.$(AWS_CURRENT_REGION_ID).amazonaws.com
	echo "Build & Push Docker image..."
	docker buildx build --platform linux/amd64 -t $(AWS_CURRENT_ACCOUNT_ID).dkr.ecr.$(AWS_CURRENT_REGION_ID).amazonaws.com/crawler:$(IMAGE_TAG) .
	# aws ecr create-repository --repository-name crawler --image-scanning-configuration scanOnPush=true
	docker push $(AWS_CURRENT_ACCOUNT_ID).dkr.ecr.$(AWS_CURRENT_REGION_ID).amazonaws.com/crawler:$(IMAGE_TAG)
	echo "Push completed successfully."

clean: # Cleanup files generated during sam building.
	@echo "Cleaning old files..."
	rm -rf /.pytest_cache
	rm -rf /__pycache
	rm -rf */.pyc
	rm -rf .mypy_cache
	@echo "Done."

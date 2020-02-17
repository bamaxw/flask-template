name="<APPNAME>"
version=$(shell git rev-parse HEAD)
semver-version=$(shell git describe --abbrev=0 --tags)
repo="<NOREPO>"
date=$(shell date -u +'%Y-%m-%dT%H:%M:%SZ')
hypothesis-profile?="default"

.PHONY: clean update-pip install-reqs install-test-reqs test create-venv check-format mypy lint check format build push-version push-latest push-semver tag-latest tag-semver

# Python
clean:
	find . -name "*.py[cod]" -delete
	find . -name "__pycache__" -delete

update-pip:
	pip3 install -U pip

install-reqs: update-pip
	pip3 install -r requirements.txt

install-test-reqs: update-pip
	pip3 install -r requirements-test.txt

test:
	pytest -vv --cov-config .coveragerc --cov -c pytest.ini --hypothesis-profile=$(hypothesis-profile) .
	coverage xml


# Python virtualenv
create-venv:
	python3 -m venv .venv


# CI
check-format:
	black --check --diff
	isort --recursive --check-only --diff .

mypy:
	mypy .

lint:
	flake8 .

check:
	make check-format
	echo
	make mypy
	echo
	make lint
	echo

format:
	black .
	isort --recursive .


# Docker
build:
	echo $(VERSION) > .commit-id
	docker build \
		--build-arg APP_NAME=$(name) \
		--build-arg VENDOR=$(vendor) \
		--build-arg DESCRIPTION=$(description) \
		--build-arg GITHUB_URL=$(github-url) \
		--build-arg BUILD_DATE=$(date) \
		--build-arg VCS_REF=$(version) \
		--build-arg SEMVER_VERSION=$(semver-version) \
		-t $(repo)/$(name):$(version)

push-version:
	docker push $(repo)/$(name):$(version)

push-latest:
	docker push $(repo)/$(name):latest

push-semver:
	docker push $(repo)/$(name):$(semver-version)

tag-latest:
	docker tag $(repo)/$(name):$(version) $(repo)/$(name):latest

tag-semver:
	docker tag $(repo)/$(name):$(version) $(repo)/$(name):$(semver-version)
export PROJECT := tuxsuite

.PHONY:all flake8 check-black black test lint-dockerfile lint-markdown
all: test test-integration flake8 check-black lint-dockerfile lint-markdown
	@echo "🚀😀👌😍🚀"

flake8:
	flake8 .

check-black:
	black --check .

black:
	black .

test:
	python3 -m pytest --cov=tuxsuite --cov-report term-missing --cov-fail-under=91 .

test-integration:
	run-parts --report test/integration

lint-dockerfile:
	docker run --rm -i hadolint/hadolint < Dockerfile

lint-markdown:
	docker run -v $$(pwd):/work -w /work --rm -i pipelinecomponents/markdownlint /work/scripts/markdownlint

docs/index.md: README.md scripts/readme2index.sh
	scripts/readme2index.sh $@

public: README.md docs/index.md mkdocs.yml $(wildcard docs/*)
	mkdocs build

serve-public: docs/index.md
	mkdocs serve --livereload --strict

# the pypi upload is automated on the CI pipeline
export flit = true
release:
	./scripts/release $(VERSION)

.PHONY: install run_tests check_format _compile _install_req _black _flake8 _isort _install_pre_commit help check_python_version clean

.DEFAULT_GOAL := help
.DELETE_ON_ERROR:

help:
	@echo "Available targets:"
	@echo "  install         : Compile and install dependencies"
	@echo "  check_format    : Run all checks and formatting"


install: _check_python_version ## compile and install dependencies
	$(MAKE) _install_req
	$(MAKE) _install_pre_commit
	$(MAKE) _install_template_project


install_develop: _check_python_version ## compile and install dependencies
	$(MAKE) _install_req
	$(MAKE) _install_pre_commit
	$(MAKE) _install_template_project_develop

_install_template_project_develop: # install template_project in editable mode
	@echo "Installing template_project in editable mode"
	cd src/ && pip install -e .

_install_template_project: # install template_project
	@echo "Installing template_project"
	cd src/ && pip install .

check_format: _black _flake8 _isort ## all checks

run_tests:
	@pytest src/

_compile: ## pip compile src/requirements.in
	@echo "Installing pip tools"
	@pip install pip-tools
	@echo "Compiling requirements"
	@pip-compile --no-emit-index-url --output-file=src/requirements.txt src/requirements.in

_install_req: _compile ## pip install requirements.txt
	@echo "Syncing requirements"
	@pip-sync src/requirements.txt

_install_pre_commit: # installs pre-commit so that it runs automatically on commit
	@echo "Setting up pre-commit"
	@pre-commit install

_black: ## check and format code with black
	@echo "Checking and formatting black"
	@black .

_flake8: ## check flake8 passes
	@echo "Checking Flake8"
	@flake8 --config setup.cfg

_isort:
	@echo "Checking and formatting isort"
	@isort .

_check_pre_commit: # run all pre-commit checks
	@pre-commit run --all-files

_check_python_version:
	@python --version | grep -q "Python 3.10" || (echo "Python 3.10 required, please install it."; exit 1)

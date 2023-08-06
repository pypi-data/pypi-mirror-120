MAKEFLAGS += -j $(shell nproc)
#MAKEFLAGS += -j $(shell nproc) -Oline
APP_NAME=epicman
# Requireds /venv so chicken and egg problem
#DETECTED_APP_VERSION=${shell venv/bin/pkginfo epicman | grep ^version | cut -f2 -d:}

VENV=venv
VENV_DIR=.venv
VENV_ROLES=environ
BUILD_TOOLS=${VENV_DIR}/venv-build-tools
PIP_CACHE=.pip-cache

SYSTEM_PYTHON=python3.9
TESTED_PYTHON_CANDIDATES=${addprefix python3.,${shell seq 7 10}}
TESTED_PYTHON_VERSIONS=${shell basename -a `which ${TESTED_PYTHON_CANDIDATES}`}

MYPY_CACHE_DIR=.mypy_cache
DMYPY_STATUS=${MYPY_CACHE_DIR}/dmypy.status

DEFAULT_SDIST = zip

HAS_COLOR=${shell tty | grep -v "not a tty" }
PYTEST_COLOR=${if $HAS_COLOR,--color=yes,}
TODO_COLOR=${if $HAS_COLOR,--force,}

BANDIT_HTML_DIR=build/bandit
COVERAGE_HTML_DIR=build/htmlcov
DOCS_SRC_DIR=docs
DOCS_DEST_DIR=build/docs/

PYTEST_PARALLEL=--workers=auto

RSYNC_REMOTE_DIR=tmp
# Taken from .hgignore
RSYNC_EXCLUDES=--exclude "*~" --exclude /.coverage --exclude /build/ --exclude ${VENV_DIR} --exclude /*-cache/ --exclude /*_cache/ --exclude *.pyc --exclude /server --exclude __pycache__/
RSYNC_REMOTE=${shell avahi-browse -c -t -l -p _build-host._tcp | sort -n -r -k 2 | head -n1 | cut -f4,6 -d\; | sed 's/;/./'}


.PHONY: help
help:
	@echo "# Makefile Commands"
	@echo ""
	@echo '``` console'
	@echo "make help         # Displays this output"
	@echo '```'
	@echo ""
	@echo "## Version Control"
	@echo "These commands are wrappers around version control to ensure tooling is updated when"
	@echo "moving between different revisions (eg pulling in remote changes that may need new"
	@echo "packages"
	@echo ""
	@echo '``` console'
	@echo "make pull         # Pull remote changes to local repo, refreshing tooling as required"
	@echo "make push         # Push local changes to default repo"
	@echo '```'
	@echo ""
	@echo "## Tooling"
	@echo "These commands are focused on providing tools to assist with code development"
	@echo ""
	@echo '``` console'
	@echo "make virtualenv   # Make a virtualenv with minimum requirements for local testing"
	@echo "make coverage     # Build a coverage venv and run coverage tests"
	@echo "make pytest       # Run the unit test suite and basic sanity checking"
	@echo "                  # Use TEST_SUITE to run a subset of tests"
	@echo "                  # eg make pytest TEST_SUITE=tests/smoke"
	@echo "make syntax-check # Run a lightweight syntax check"
	@echo "make flake8       # Perform basic linting, import checks and variable usage checks"
	@echo "make mypy         # Perform a type check"
	@echo "make pyright      # Perform a type check using Microsofts pyright tool"
	@echo "make bandit       # Perform a security check with the bandit project"
	@echo "make test         # Run all checks"
	@echo "make readme_check # Confirm the README is valid markdown"
	@echo "make todo         # Get a list of TODO and BUG items"
	@echo '```'
	@echo ""
	@echo "## Remote Commands"
	@echo "Some commands have 'remote' equivalents to allow them to be run on different servers"
	@echo "that are faster or have a different architecture (eg for testing multiple platforms)."
	@echo "These commands all take a single argument 'RSYNC_REMOTE' used to specify where to run"
	@echo "in the form user@host. The user@ part may optionally omitted if the local and remote"
	@echo "hosts match"
	@echo ""
	@echo "### Examples"
	@echo '``` console'
	@echo "make pytest-remote RSYNC_REMOTE=parallels@build-1.local"
	@echo "make docs-remote RSYNC_REMOTE=parallels@build-1.local"
	@echo '```'
	@echo ""
	@echo "## Build Commands"
	@echo "These commands are focused around building artefacts for final release and installation"
	@echo "in local virtualenvs"
	@echo ""
	@echo '``` console'
	@echo "make sdist        # Build a source bundle"
	@echo "make bdist        # Build a wheel for distribution"
	@echo "make docs         # Build the docs"
	@echo '```'
	@echo ""
	@echo "## Release Commands"
	@echo "Note: these may require credentials such as ssh keys or pip passwords to complete"
	@echo ""
	@echo '``` console'
	@echo "make docs-deploy  # Build and push docs to http://docs.epicman.com"
	@echo "make push         # Push local changes to default repo"
	@echo "make pypi         # Release source and wheel dists to pypi"
	@echo "make release      # Perform a full test and build and upload all artefacts"
	@echo '```'

## VirtualEnv setups
.PHONY: virtualenv
virtualenv: $(VENV)
${VENV}: ${VENV_DIR}/venv-build-tools
	ln -s $< $@
### Base virtual environments
${VENV_DIR}/venv-%: ${VENV_ROLES}/common.txt ${VENV_ROLES}/%.txt setup.cfg | ${VENV_DIR} ${PIP_CACHE}
	${SYSTEM_PYTHON} -m venv $@
	$@/bin/pip --cache-dir ${PIP_CACHE} install wheel
	$@/bin/pip --cache-dir ${PIP_CACHE} install -r $<
	-$@/bin/pip --cache-dir ${PIP_CACHE} install -r ${VENV_ROLES}/$*.txt
	touch $@
### Per Python environments for test suite
${VENV_DIR}/python%: ${VENV_ROLES}/common.txt ${VENV_ROLES}/pytest.txt setup.cfg | ${VENV_DIR} ${PIP_CACHE}
	python$* -m venv $@
	$@/bin/pip --cache-dir ${PIP_CACHE} install wheel
	$@/bin/pip --cache-dir ${PIP_CACHE} install ${addprefix -r ,$^}
	touch $@
${VENV_DIR}:
	mkdir $@
${PIP_CACHE}:
	mkdir -p $@

## Build
.PHONY: build
build: bdist

.PHONY: bdist
bdist: ${BUILD_TOOLS}
	$</bin/python -m build --wheel

.PHONY: sdist
sdist: ${BUILD_TOOLS}
	$</bin/python -m build --sdist

.PHONY: pyright
pyright: ${VENV_DIR}/venv-pyright
	$</bin/pyright ${APP_NAME} 

.PHONY: mypy
mypy: ${BUILD_TOOLS} dmypy
	$</bin/dmypy --status-file ${DMYPY_STATUS} check -- ${APP_NAME}

${MYPY_CACHE_DIR}:
	mkdir $@

.PHONY: dmypy
dmypy: ${DMYPY_STATUS}
${DMYPY_STATUS}: ${BUILD_TOOLS} ${MYPY_CACHE_DIR}
	$</bin/dmypy --status-file "$@" start --timeout 1800 -- --exclude=__main__.py --pretty -p ${APP_NAME}

.PHONY: bandit
bandit: ${VENV_DIR}/venv-bandit ${APP_NAME}
	$</bin/bandit -r ${APP_NAME}
.PHONY: bandit-html
bandit-html: ${BANDIT_HTML_DIR}
${BANDIT_HTML_DIR}: ${VENV_DIR}/venv-bandit ${APP_NAME}
	mkdir -p $@
	-$</bin/bandit -f html -r ${APP_NAME} > $@/index.html
bandit-json: build/bandit.json
build/bandit.json: ${VENV_DIR}/venv-bandit ${APP_NAME}
	-$</bin/bandit -f json -r ${APP_NAME} > $@

flake8: ${BUILD_TOOLS}
	$</bin/flake8 `find ${APP_NAME} -type f -iname \*.py`

pylint: ${BUILD_TOOLS}
	$</bin/pylint ${APP_NAME}

.PHONY: test
test: build syntax-check flake8 pylint mypy pytest

## Pytest
.PHONY: pytest
pytest: ${VENV_DIR}/venv-pytest
	PYTHONPATH=. $</bin/pytest ${PYTEST_PARALLEL} ${PYTEST_COLOR} ${PYTEST_ARGS} ${TEST_SUITE}

.PHONY: pytest-remote
pytest-remote: rsync
	ssh ${RSYNC_REMOTE} -t -- "cd ${RSYNC_REMOTE_DIR}/${APP_NAME}; make pytest ${MAKEFLAGS}"

.PHONY: pytest-all
pytest-all: $(addprefix pytest-,${TESTED_PYTHON_VERSIONS})
	echo ${TESTED_PYTHON_CANDIDATES}
	echo ${TESTED_PYTHON_VERSIONS}
	echo $^
pytest-%: ${VENV_DIR}/%
	PYTHONPATH=. $</bin/pytest ${PYTEST_PARALLEL} ${PYTEST_COLOR} ${PYTEST_ARGS} ${TEST_SUITE}
tests/%.py: .FORCE
	${MAKE} pytest TEST_SUITE="tests/$*.py"

## Coverage
.PHONY: coverage coverage-html
coverage:
	${MAKE} pytest PYTEST_ARGS="--cov-report=term"
coverage-html: ${COVERAGE_HTML_DIR}
${COVERAGE_HTML_DIR}: ${APP_NAME} tests
	-${MAKE} pytest PYTEST_ARGS="--cov --cov-report=html:$@"
	touch -c $@

## Syntax Check
.PHONY: syntax-check
syntax syntax-check sanity: ${BUILD_TOOLS}
	$</bin/python -m compileall ${APP_NAME}

.PHONY: clean
clean:
	-rm -r ${APP_NAME}/**/__pycache__
	-rm -r ${APP_NAME}/**/*.pyc
	-rm -rf dist build *.egg-info
	-rm ${SRC_DIR}/*.o ${SRC_DIR}/*.so
	-rm -t ${VENV_DIR} ${VENV}

#######
# Docs
.PHONY: docs ${DOCS_DEST_DIR}
docs: ${DOCS_DEST_DIR} 

.PHONY: docs-remote
docs-remote: rsync
	ssh ${RSYNC_REMOTE} -t -- "cd ${RSYNC_REMOTE_DIR}/${APP_NAME}; make docs"
	rsync -av --info=progress2 ${RSYNC_REMOTE}:${RSYNC_REMOTE_DIR}/${APP_NAME}/${DOCS_DEST_DIR} ${DOCS_DEST_DIR}

GEN_DOCS=makefile.md todo.md bugs.md cli_output.md bandit.md
${DOCS_DEST_DIR}: ${VENV_DIR}/venv-docs $(addprefix ${DOCS_SRC_DIR}/,${GEN_DOCS}) ${COVERAGE_HTML_DIR}
	mkdir -p $@
	$</bin/mkdocs build --strict --clean -d $@
	touch -c $@

# depend on ourselves as we need to ensure the file gets updates when the help does
${DOCS_SRC_DIR}/makefile.md: Makefile
	${MAKE} -s help > $@

${DOCS_SRC_DIR}/todo.md: ${BUILD_TOOLS} ${APP_NAME} .FORCE
	$</bin/python bin/todo todo "${APP_NAME}" > "$@"

${DOCS_SRC_DIR}/bugs.md: ${BUILD_TOOLS} ${APP_NAME} .FORCE
	$</bin/python bin/todo bugs "${APP_NAME}" > "$@"

${DOCS_SRC_DIR}/roadmap.md: ${BUILD_TOOLS} ${APP_NAME} .FORCE
	$</bin/python bin/todo plan "${APP_NAME}" > "$@"

${DOCS_SRC_DIR}/cli_output.md: ${BUILD_TOOLS} ${APP_NAME} .FORCE
	$</bin/python -m ${APP_NAME}.server --help > "$@"

docs/%.md: docs/%.md.j2 build/%.json
	${VENV_DIR}/venv-docs/bin/python bin/template build/$*.json $< > $@

.PHONY: docs-serve
docs-serve: ${VENV_DIR}/venv-docs ${DOCS_DEST_DIR}
	$</bin/python -m http.server -d ${DOCS_DEST_DIR}

docs-deploy: ${DOCS_DEST_DIR}
	rsync -azv --delete --info=progress2  $< docs.epic-man.net:sites/docs.epic-man

#######
# PyPI
pypi: ${BUILD_TOOLS} build readme_check
	$</bin/twine upload --non-interactive --skip-existing dist/*.whl dist/*.tar.gz

# use the sdist for speed as bdist: sdist
readme_check: ${BUILD_TOOLS} sdist
	$</bin/twine check --strict dist/*gz

release: build public push
	# Ensure the version to be released is taggged with a proper version number
	test "`hg log --no-stat -r tip~1 --template "{tags}\n" | grep -o -E '(v[0-9][.0-9]*+)'`"
	${MAKE} docs-deploy
	${MAKE} pypi

pull:
	hg pull

push: | public
	hg push

public:
	hg phase -p

########
# Utils
.PHONY: linecount
linecount:
	wc -l `find ${APP_NAME} -type f -name '*py'`

.PHONY: todo
todo:
	./bin/todo ${TODO_COLOR} todo ${APP_NAME}

watch-pytest:
	$(MAKE) -e WATCHER_DIRS="${APP_NAME} tests" -e  WATCHER_CMD="make pytest" watcher

watch-docs:
	$(MAKE) -e WATCHER_DIRS="docs mkdocs.yml" -e  WATCHER_CMD="$${MAKE} docs" watcher

watcher:
	@while true; do \
	    inotifywait -qq -r -e close_write -e move -e delete -e delete_self ${WATCHER_DIRS} ;\
	    sleep 1 ;\
	    ${WATCHER_CMD} || echo '\a' ;\
	done

.PHONY: rsync
rsync:
	test -n "${RSYNC_REMOTE}"
	rsync ${RSYNC_EXCLUDES} -av --info=progress2 . ${RSYNC_REMOTE}:${RSYNC_REMOTE_DIR}/${APP_NAME}/

.FORCE:

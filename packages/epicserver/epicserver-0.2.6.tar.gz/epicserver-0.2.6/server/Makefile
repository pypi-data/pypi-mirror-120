DEFAULT_HOSTS=1.build.epic-man.net
DEFAULT_PLAY=setup-server.yml

SYSTEM_PYTHON=python3
PYTHON=${VENV}/bin/python

VENV=venv

setup: ${VENV}
	$</bin/ansible-playbook -i inventory --limit ${DEFAULT_HOSTS} ${DEFAULT_PLAY}
setup-%: ${VENV}
	$</bin/ansible-playbook -i inventory --limit ${DEFAULT_HOSTS} setup-$*.yml

virtualvenv: ${VENV}
${VENV}: deploy-tools.txt
	${SYSTEM_PYTHON} -m venv $@
	${PYTHON} -m pip install wheel
	${PYTHON} -m pip install -r $<

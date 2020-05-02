VENV_DIR=venv
VENV_BIN=${VENV_DIR}/bin
VENV_PIP=${VENV_BIN}/pip3
VENV_YAPF=${VENV_BIN}/yapf

venv:
	python3.7 -m venv ${VENV_DIR}
	${VENV_PIP} install -r requirements.txt

format:
	${VENV_YAPF} -i *.py

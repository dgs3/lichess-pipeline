VENV_DIR=venv
VENV_BIN=${VENV_DIR}/bin
VENV_PIP=${VENV_BIN}/pip3
VENV_YAPF=${VENV_BIN}/yapf
VENV_LINT=${VENV_BIN}/pylint
VENV_PYTHON=${VENV_BIN}/python3.7

venv:
	python3.7 -m venv ${VENV_DIR}
	${VENV_PIP} install -r requirements.txt

format:
	${VENV_YAPF} -i *.py scripts/*.py

lint:
	${VENV_LINT} --rcfile=pylintrc *.py scripts/*.py

pipeline: venv
	${VENV_PYTHON} pipeline.py --local

pipeline-fresh: venv
	${VENV_PYTHON} pipeline.py lichess_fresh --local

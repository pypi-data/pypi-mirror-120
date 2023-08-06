#!/bin/bash

function errexit(){
  echo "$@" >&2
  exit 1
}

SCRIPT=$(readlink -f "$0")
FOLDER=$(dirname "$SCRIPT")
VENV="${FOLDER}/py3venv"
cd "${FOLDER}" || errexit "FATAL BUG: script exists but parent directory doesn't."



function run(){
  local action="$1"
  shift
  echo "ACTION: ${action}"
  echo "  RUN:  $*"
  "$@" &> ./op.log
  local rc=$?

  if [ "$rc" == 0 ]; then
    echo "  RESULT: success"
  else
    echo "  RESULT: error (RC=$rc)"
    sed 's/^/  | /' ./op.log
    errexit "Error: action '$action' failed."
  fi
}

function do_action(){
  case "$1" in
    rebuild-venv)
      rm -rf "${VENV}"
      "${SCRIPT}" build-venv
    ;;

    build-venv)
      if [ ! -d "${VENV}" ]; then
        python3 -m venv "${VENV}"           || errexit "Error: can't create python3 virtual environment at '${VENV}'."
      fi
      . "${VENV}/bin/activate"              || errexit "Error: can't activate python3 virtual environment."
      pip install --upgrade pip             || errexit "Error: can't upgrade python3 pip."
      pip install -r "requirements-dev.txt" || errexit "Error: can't install development requirements."
      pip install -r "requirements.txt"     || errexit "Error: can't install runtime requirements."
      python "${FOLDER}/setup.py" develop   || errexit "Error: can't install runtime requirements."
    ;;

    test)
      shift
      tox -vv "$@"
    ;;

    test-envs)
      shift
      envs="$*"
      tox -vv -e ${envs// /,}
    ;;

    test-py-all)
      shift
      tox -vv "$@" -e py36,py37,py38,py39
    ;;

    test-style-quality)
      shift
      tox -vv "$@" -e style,quality
    ;;

    test-coverage)
      shift
      tox -vv "$@" -e coverage
    ;;

    unit-test)
      shift
      export PYTHONUNBUFFERED=yes
      pytest -vv --basetemp="${FOLDER}/tests" "$@"
    ;;

    coverage)
      shift
      run "Generate Coverage Data" pytest --cov-config=./.coveragerc --cov=pt.ptutils --cov-report html -vv --basetemp="${FOLDER}/src" "$@"
    ;;

    docs)
      shift
      do_action coverage
      run "Build Documentation" python3 setup.py build_sphinx "$@"
    ;;

    quality)
      shift
      do_action coverage
      run "Compute Cyclomatic Complexity (CC)" radon cc -i '__pending*' ./src
      run "Compute Maintainability Index (MI)" radon mi -i '__pending*' ./src
      run "Compute raw statistics (RAW)" radon raw -i '__pending*' ./src
      run "Analyze Code Quality" xenon -b C -m A -a A -i '__pending*' ./src
    ;;

    style)
      shift
      export PYTHONUNBUFFERED=yes
      run "Check Source code Style Compliance" flake8 --max-line-length=120 --ignore=E201,E202,E401,E221,E241,W504 --exclude '__pending*' src
    ;;

    *)
      errexit "Unknown action '$1'"
    ;;
  esac
}

do_action "$@"
#!/bin/sh
#set -x

ROOT="$(dirname "$(readlink -f "$0")")"
SCRIPT=$(basename "$0")
VENV="${ROOT}/venv"

_inspect () {
  # Auto generate help string
  local help=$(awk '$1 ~ /^[a-z]+_?[a-z]+$/ && $2 == "()" { printf "%s|", $1 }' $0)
  echo ${help%|}
}

_is_exe () {
  command -v $1 >/dev/null 2>&1 || \
    { echo >&2 "missing $1 command"; return 1; }; return 0
  }
#-----------------------------------------------------------------------------#

_mkvenv () {
  echo Setting up python virtualenv
  _is_exe python3 || exit 1
  python3 -m venv "${VENV}"
  . "${VENV}/bin/activate"
  pip install Flask
}

_get_jquery () {
  mkdir -p static/js/
  wget -O "${ROOT}/static/js/jquery-3.3.1.min.js" https://code.jquery.com/jquery-3.3.1.min.js
}

_get_bootstrap () {
  mkdir -p "${ROOT}/static/bootstrap"
  wget https://github.com/twbs/bootstrap/releases/download/v4.1.0/bootstrap-4.1.0-dist.zip -O /tmp/bootstrap-4.1.0-dist.zip
  cd "${ROOT}/static/bootstrap" && unzip /tmp/bootstrap-4.1.0-dist.zip && rm /tmp/bootstrap-4.1.0-dist.zip
}
_get_forkawesome () {
  wget https://github.com/ForkAwesome/Fork-Awesome/archive/1.0.11.zip -O  /tmp/1.0.11.zip
  unzip /tmp/1.0.11.zip -d "${ROOT}/static/"
}

get_libs () {
  _get_jquery
  _get_popper
  _get_bootstrap
}

serve () {
  #FLASK_APP=app FLASK_ENV=development flask run
  DEBUG=Y python3 "${ROOT}/app.py"
}

python_shell () {
  python3 -ic"import app;print('Use exit() or Ctrl-D to exit')"
}

if [ ! -e "${VENV}/bin/activate" ];then
    _mkvenv
else
    . "${VENV}/bin/activate"
fi

if [ $# -eq 0 ]
then
  echo "${ROOT}/${SCRIPT} $(_inspect)"
  exit
fi


$@

# vim: fileencoding=utf8 ft=sh

template = """#!/bin/bash 
#-xe
export DIR_VENV=$PWD/_venv

if [ -d "$DIR_VENV" ]; then
  source $DIR_VENV/bin/activate
fi

cmd_install() {
  # installar. Tambien se puede usar para actualizar agregadas librerias
  if [ ! -d "$DIR_VENV" ]; then
    # sudo apt-get install python3-venv -y
    python3 -m venv $DIR_VENV
  fi
  
  if [ -f "requirements-lock.txt" ]; then
    $DIR_VENV/bin/pip install -r requirements-lock.txt
  fi

  $DIR_VENV/bin/pip install -r requirements.txt
  $DIR_VENV/bin/pip freeze -r requirements.txt > requirements-lock.txt
}

cmd_add() {
  # agregar paquetes
  $DIR_VENV/bin/pip install $@
  $DIR_VENV/bin/pip freeze -r requirements.txt > requirements-lock.txt
}

cmd_add-mg() {
  # agregar paquetes & buscarlo primero en el pypi maujagroup 
  $DIR_VENV/bin/pip install $@ -i http://pypi.maujagroup.com:8080/simple\
    --trusted-host pypi.maujagroup.com\
    --extra-index-url https://pypi.org/simple

  $DIR_VENV/bin/pip freeze -r requirements.txt > requirements-lock.txt
}

cmd_lock() {
  # crear lock
  $DIR_VENV/bin/pip freeze -r requirements.txt > requirements-lock.txt
}

cmd_del() {
  # agregar paquetes
  $DIR_VENV/bin/pip uninstall $@
  $DIR_VENV/bin/pip freeze -r requirements.txt > requirements-lock.txt
}


cmd_web() { 
  python3 web.py 
}

cmd_webdev() { 
  python3 web.py --dev
}

cmd_cmd() { 
  python3 cmd.py "$@" 
}

cmd_migrate() { 
  python3 migrate.py "$@" 
}

cmd_pip() { 
  pip "$@" 
}

cmd_pos-commit() { 
    echo "pos-commit";
}

cmd_version() {
  python --version
  pip --version
}

cd "$(dirname "$0")"; _cmd="${1?"cmd is required"}"; shift; "cmd_${_cmd}" "$@"
"""

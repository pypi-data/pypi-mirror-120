template = """
#!/bin/bash 
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
  $DIR_VENV/bin/pip install -r requirements.txt
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

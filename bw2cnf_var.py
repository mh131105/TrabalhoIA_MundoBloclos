"""Compatibilidade: executa a implementação na pasta de entrega."""
import runpy
import sys
from pathlib import Path

project = Path(__file__).resolve().parent / "TrabalhoIA_MundoBloclos_equipe_20"
sys.path.insert(0, str(project))
runpy.run_path(str(project / "bw2cnf_var.py"), run_name="__main__")

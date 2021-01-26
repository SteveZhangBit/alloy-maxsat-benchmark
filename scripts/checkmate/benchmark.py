import subprocess
import os
from os import path
import shutil
import signal
import sys

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from util import run_sat, run_maxsat


if __name__ == "__main__":    
  print("name,maxsat,maxsat_part,sat,#inst")
  for name in ["flush_reload", "meltdown", "spectre"]:
    name = sys.argv[1]
    print(name + ",", end="")

    maxsat_result = run_maxsat(name + "_maxsat.als", 30*60)
    print(maxsat_result + ",", end="")

    sat_result = run_sat(name + ".als", 30*60)
    print(f"{name},{maxsat_result},{sat_result}")

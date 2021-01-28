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
  timeout = 30 * 60
  for name in ["flush_reload", "meltdown", "spectre"]:
    for _ in range(5):
      maxsat_time = run_maxsat(name + "_maxsat.als", timeout=timeout)
      maxsat_part_time = run_maxsat(name + "_maxsat.als", timeout=timeout, partition=True)
      sat_time = run_sat(name + ".als", timeout=timeout)
      print(f"{name},{maxsat_time},{maxsat_part_time},{sat_time}")

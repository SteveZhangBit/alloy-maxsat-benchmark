import subprocess
import os
from os import path
import shutil
import signal
import sys

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from util import run_sat, run_maxsat


if __name__ == "__main__":
  print("problem,maxsat_trans,maxsat_total,maxsat_result,maxsat_part_trans,maxsat_part_total,maxsat_part_result,sat_trans,sat_total,#inst")
  timeout = 30 * 60
  repeat = 5
  for name in ["flush_reload", "meltdown", "spectre"]:
    for _ in range(repeat):
      maxsat_results = run_maxsat(name + "_maxsat.als", timeout=timeout)
      maxsat_part_results = run_maxsat(name + "_maxsat.als", timeout=timeout, partition=True)
      sat_results = run_sat(name + ".als", timeout=timeout)
      print(f"{name},{maxsat_results},{maxsat_part_results},{sat_results}")

import subprocess
import os
from os import path
import shutil
import signal
import sys


def run_sat(sat, timeout=60, sat_scale=2):
  cmd = [
    "java",
    "-Xms8192k",
    "-Xmx4096m",
    "-Djava.library.path=../../lib/open-wbo",
    "-cp",
    "../../bin/org.alloytools.alloy.dist.jar",
    "edu.mit.csail.sdg.alloy4whole.BenchmarkMain",
    "-t=" + str(timeout),
    "-m=" + str(sat_scale),
    "-sat=" + sat
  ]

  with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, preexec_fn=os.setsid) as proc:
    result = "N/A,N/A"
    sat_time = "N/A"
    num_inst = "N/A"
    try:
      out = proc.communicate()[0]
      for line in out.strip().split("\n"):
        if line.startswith("Enumeration time: "):
          sat_time = line[18:]
        elif line.startswith("Enumeration number: "):
          num_inst = line[20:]
      result = f"{sat_time},{num_inst}"
    except Exception as e:
      os.killpg(proc.pid, signal.SIGINT)
      proc.communicate()
      raise e
  return result

def run_maxsat(maxsat, timeout=60):
  cmd = [
    "java",
    "-Xms8192k",
    "-Xmx4096m",
    "-Djava.library.path=../../lib/open-wbo",
    "-cp",
    "../../bin/org.alloytools.alloy.dist.jar",
    "edu.mit.csail.sdg.alloy4whole.BenchmarkMain",
    "-t=" + str(timeout),
    "-maxsat=" + maxsat
  ]

  with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, preexec_fn=os.setsid) as proc:
    result = "N/A,N/A"
    maxsat_time = "N/A"
    maxsat_part_time = "N/A"
    try:
      out = proc.communicate()[0]  
      for line in out.strip().split("\n"):
        if line.startswith("MaxSat time: "):
          maxsat_time = line[13:]
        elif line.startswith("MaxSat-Partition time: "):
          maxsat_part_time = line[23:]
      result = f"{maxsat_time},{maxsat_part_time}"
    except Exception as e: 
      os.killpg(proc.pid, signal.SIGINT)
      proc.communicate()
      raise e
  return result

import subprocess
import os
from os import path
import shutil
import signal
import sys


def run_sat(sat, timeout=60):
  cmd = [
    "java",
    "-Xms8192k",
    "-Xmx4096m",
    "-Djava.library.path=../../lib/open-wbo",
    "-cp",
    "../../bin/org.alloytools.alloy.dist.jar",
    "edu.mit.csail.sdg.alloy4whole.BenchmarkMain",
    "-sat=" + sat
  ]

  with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, preexec_fn=os.setsid) as proc:
    result = "N/A,N/A"
    sat_time = "N/A"
    num_inst = "N/A"
    try:
      out = proc.communicate(timeout=timeout)[0]
      for line in out.strip().split("\n"):
        if line.startswith("Enumeration time: "):
          sat_time = line[18:]
        elif line.startswith("Enumeration number: "):
          num_inst = line[20:]
      result = f"{sat_time},{num_inst}"
    except subprocess.TimeoutExpired:
      os.killpg(proc.pid, signal.SIGINT)
    except Exception as e:
      os.killpg(proc.pid, signal.SIGINT)
      proc.communicate()
      raise e
  return result


def run_maxsat(maxsat, timeout=60, partition=False):
  cmd = [
    "java",
    "-Xms8192k",
    "-Xmx4096m",
    "-Djava.library.path=../../lib/open-wbo",
    "-cp",
    "../../bin/org.alloytools.alloy.dist.jar",
    "edu.mit.csail.sdg.alloy4whole.BenchmarkMain",
    "-maxsat=" + maxsat
  ]
  if partition:
    cmd.append("-p")

  with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, preexec_fn=os.setsid) as proc:
    result = "N/A"
    try:
      out = proc.communicate(timeout=timeout)[0]
      if partition:
        for line in out.strip().split("\n"):
          if line.startswith("MaxSat-Partition time: "):
            result = line[23:]
            break
      else:
        for line in out.strip().split("\n"):
          if line.startswith("MaxSat time: "):
            result = line[13:]
            break
    except subprocess.TimeoutExpired:
      os.killpg(proc.pid, signal.SIGINT)
    except Exception as e:
      os.killpg(proc.pid, signal.SIGINT)
      proc.communicate()
      raise e
  return result

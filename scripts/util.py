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
    "-Xmx8192m",
    "-Djava.library.path=../../lib/open-wbo",
    "-cp",
    "../../bin/org.alloytools.alloy.dist.jar",
    "edu.mit.csail.sdg.alloy4whole.BenchmarkMain",
    "-sat=" + sat
  ]

  trans_time = "N/A"
  total_time = "N/A"
  num_inst = "N/A"
  with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, preexec_fn=os.setsid) as proc:
    try:
      out = proc.communicate(timeout=timeout)[0]
      for line in out.strip().split("\n"):
        if line.startswith("Translation time: "):
          trans_time = line[len("Translation time: "):]
        elif line.startswith("Total time: "):
          total_time = line[len("Total time: "):]
        elif line.startswith("Enumeration number: "):
          num_inst = line[len("Enumeration number: "):]
    except subprocess.TimeoutExpired:
      os.killpg(proc.pid, signal.SIGINT)
      out = proc.communicate()[0]
      for line in out.strip().split("\n"):
        if line.startswith("Enumeration number: "):
          num_inst = line[len("Enumeration number: "):]
          break
    except Exception as e:
      os.killpg(proc.pid, signal.SIGINT)
      proc.communicate()
      raise e
  return f"{trans_time},{total_time},{num_inst}"


def run_maxsat(maxsat, timeout=60, partition=False):
  cmd = [
    "java",
    "-Xms8192k",
    "-Xmx8192m",
    "-Djava.library.path=../../lib/open-wbo",
    "-cp",
    "../../bin/org.alloytools.alloy.dist.jar",
    "edu.mit.csail.sdg.alloy4whole.BenchmarkMain",
    "-maxsat=" + maxsat
  ]
  if partition:
    cmd.append("-p")

  trans_time = "N/A"
  total_time = "N/A"
  sat = "N/A"
  with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, preexec_fn=os.setsid) as proc:
    try:
      out = proc.communicate(timeout=timeout)[0]
      for line in out.strip().split("\n"):
        if line.startswith("Translation time: "):
          trans_time = line[len("Translation time: "):]
        elif line.startswith("Total time: "):
          total_time = line[len("Total time: "):]
        elif line.startswith("Solved: "):
          sat = line[len("Solved: "):]
    except subprocess.TimeoutExpired:
      os.killpg(proc.pid, signal.SIGINT)
    except Exception as e:
      os.killpg(proc.pid, signal.SIGINT)
      proc.communicate()
      raise e
  return f"{trans_time},{total_time},{sat}"

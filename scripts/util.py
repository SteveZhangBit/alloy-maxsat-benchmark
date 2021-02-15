import subprocess
import os
from os import path
import shutil
import signal
import sys
import time


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
  solve_time = "N/A"
  num_inst = "N/A"
  with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, preexec_fn=os.setsid) as proc:
    try:
      out = proc.communicate(timeout=timeout)[0]
      total_time = 0
      for line in out.strip().split("\n"):
        if line.startswith("Translation time: "):
          trans_time = int(line[len("Translation time: "):])
        elif line.startswith("Total time: "):
          total_time = int(line[len("Total time: "):])
        elif line.startswith("Enumeration number: "):
          num_inst = line[len("Enumeration number: "):]
      if total_time > 0:
        solve_time = total_time - trans_time
    except subprocess.TimeoutExpired:
      os.killpg(proc.pid, signal.SIGINT)
      out = proc.communicate()[0]
      for line in out.strip().split("\n"):
        if line.startswith("Translation time: "):
          trans_time = line[len("Translation time: "):]
        elif line.startswith("Enumeration number: "):
          num_inst = line[len("Enumeration number: "):]
    except KeyboardInterrupt as e:
      os.killpg(proc.pid, signal.SIGKILL)
      proc.communicate()
      cleantmp()
      raise e
  
  cleantmp()
  return f"{trans_time},{solve_time},{num_inst}"


def run_maxsat(maxsat, timeout=60, partition=False, auto=False):
  assert(not auto or partition)
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
  if auto:
    cmd.append("-auto")

  trans_time = "N/A"
  solve_time = "N/A"
  sat = "N/A"
  with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, preexec_fn=os.setsid) as proc:
    try:
      out = proc.communicate(timeout=timeout)[0]
      total_time = 0
      for line in out.strip().split("\n"):
        if line.startswith("Translation time: "):
          trans_time = int(line[len("Translation time: "):])
        elif line.startswith("Total time: "):
          total_time = int(line[len("Total time: "):])
        elif line.startswith("Solved: "):
          sat = line[len("Solved: "):]
      if total_time > 0:
        solve_time = total_time - trans_time
    except subprocess.TimeoutExpired:
      os.killpg(proc.pid, signal.SIGINT)
      out = proc.communicate()[0]
      for line in out.strip().split("\n"):
        if line.startswith("Translation time: "):
          trans_time = line[len("Translation time: "):]
          break
    except KeyboardInterrupt as e:
      os.killpg(proc.pid, signal.SIGKILL)
      proc.communicate()
      cleantmp()
      raise e
  
  cleantmp()
  return f"{trans_time},{solve_time},{sat}"


def run_maxsat_all(maxsat, timeout=60):
  cmd = [
    "java",
    "-Xms8192k",
    "-Xmx8192m",
    "-Djava.library.path=../../lib/open-wbo",
    "-cp",
    "../../bin/org.alloytools.alloy.dist.jar",
    "edu.mit.csail.sdg.alloy4whole.BenchmarkMain",
    "-maxsat=" + maxsat,
    "-all-opt"
  ]

  cnf = None
  trans_time = "N/A"
  solve_time = "N/A"
  num_inst = "N/A"
  out = subprocess.check_output(cmd, text=True)
  for line in out.strip().split("\n"):
    if line.startswith("Translation time: "):
      trans_time = int(line[len("Translation time: "):])
    elif line.startswith("CNF File: "):
      cnf = line[len("CNF File: "):]
  
  if cnf is not None:
    openwbo = [
      "../../lib/open-wbo/open-wbo",
      "-formula=0",
      "-algorithm=2",
      "-all-opt",
      cnf
    ]

    start_time = time.time()
    with subprocess.Popen(openwbo, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, preexec_fn=os.setsid) as proc:
      try:
        out = proc.communicate(timeout=timeout)[0]
        solve_time = round((time.time() - start_time) * 1000)
        for line in out.strip().split("\n"):
          if line.startswith("c Optimal Solutions: "):
            num_inst = line[len("c Optimal Solutions: "):]
            break
      except subprocess.TimeoutExpired:
        os.killpg(proc.pid, signal.SIGINT)
        out = proc.communicate()[0]
      except KeyboardInterrupt as e:
        os.killpg(proc.pid, signal.SIGKILL)
        proc.communicate()
        cleantmp()
        raise e

  cleantmp()
  return f"{trans_time},{solve_time},{num_inst}"


def benchmark(problems, sat_files=None, maxsat_files=None, maxsat_one=False, maxsat_all=False,
              maxsat_part=False, maxsat_part_auto=False, timeout=180, repeat=5):
  header = "problem"
  if maxsat_files is not None:
    if maxsat_one:
      header += ",maxsat_trans,maxsat_solve,maxsat_result"
    if maxsat_all:
      header += ",all_opt_trans,all_opt_solve,#opt_inst"
    if maxsat_part:
      header += ",part_trans,part_solve,part_result"
    if maxsat_part_auto:
      header += ",auto_part_trans,auto_part_solve,auto_part_result"
  if sat_files is not None:
    header += ",sat_trans,sat_solve,#inst"
  
  print(header)
  for i in range(len(problems)):
    for _ in range(repeat):
      results = problems[i]
      if maxsat_files is not None:
        if maxsat_one:
          results += "," + run_maxsat(maxsat_files[i], timeout=timeout)
        if maxsat_all:
          results += "," + run_maxsat_all(maxsat_files[i], timeout=timeout)
        if maxsat_part:
          results += "," + run_maxsat(maxsat_files[i], timeout=timeout, partition=True)
        if maxsat_part_auto:
          results += "," + run_maxsat(maxsat_files[i], timeout=timeout, partition=True, auto=True)
      if sat_files is not None:
        results += "," + run_sat(sat_files[i], timeout=timeout)
      print(results)


def options():
  run_sat = False
  run_maxsat_one = False
  run_maxsat_all = False
  run_maxsat_part = False
  run_maxsat_part_auto = False
  timeout = 180
  repeat = 5
  model = None

  if len(sys.argv) < 2:
    print("Usage: benchmark.py")
    print("\t-sat\t\t\tEnumerate all solutions by using SAT")
    print("\t-maxsat\t\t\tFind one optimal solution")
    print("\t-maxsat_all\t\tFind all optimal solutions")
    print("\t-maxsat_part\t\tFind one optimal solution by using Max-SAT with user partitioning")
    print("\t-maxsat_part_auto\tFind one optimal solution by using auto partitioning")
    print("\t-t=<timeout>")
    print("\t-r=<repeat>")
    print("\t-m=<model path>")
    exit(0)
  else:
    for arg in sys.argv[1:]:
      if arg == "-sat":
        run_sat = True
      elif arg == "-maxsat":
        run_maxsat_one = True
      elif arg == "-maxsat_all":
        run_maxsat_all = True
      elif arg == "-maxsat_part":
        run_maxsat_part = True
      elif arg == "-maxsat_part_auto":
        run_maxsat_part_auto = True
      elif arg.startswith("-t="):
        timeout = int(arg[len("-t="):])
      elif arg.startswith("-r="):
        repeat = int(arg[len("-r="):])
      elif arg.startswith("-m="):
        model = arg[len("-m="):]
  
  return run_sat, run_maxsat_one, run_maxsat_all, run_maxsat_part, run_maxsat_part_auto, timeout, repeat, model


def cleantmp():
  # FIXME: this is wrong when the user open two benchmarks at the same time, this will
  # delete the tmp files generated for the other benchmark
  tmps = filter(lambda x: x.startswith("kodkod") or x.endswith("cnf"), os.listdir("/tmp"))
  for t in tmps:
    t = path.join("/tmp", t)
    os.remove(t)

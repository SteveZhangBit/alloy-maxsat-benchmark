import subprocess
import os
from os import path
import shutil
import signal
import sys

from random import randint
from random import random

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from util import run_sat, run_maxsat

def generate(tags, persons, max_tags, num_tables, min_persons, max_persons):
  person_tags = []
  for x in range(0, persons):
    x_tags = []
    value = randint(0, max_tags)
    t=0
    for y in range (0, tags):
      if t == max_tags:
        break
      v = random()
      if v <= float(value / tags):
        x_tags.append("P" + str(x) + "->" + "T" + str(y))
        t = t + 1
    if len(x_tags) > 0:
      person_tags.append("+".join(x_tags))
  person_tags = "+\n    ".join(person_tags)
  
  als = f"""
abstract sig Person {{
  tags: set Tag
}}
one sig {",".join(["P" + str(i) for i in range(persons)])} extends Person {{}}

abstract sig Tag {{}}
one sig {",".join(["T" + str(i) for i in range(tags)])} extends Tag {{}}

fact {{
  tags = {person_tags}
}}

sig Table {{
  seat: set Person,
}} {{
  #seat < {max_persons + 1}
  #seat > {min_persons - 1}
}}

fact {{
  all p: Person | one seat.p
}}
"""
  
  sat = als + f"""
run {{}} for {num_tables} Table, 5 int
"""

  table_based = als + f"""
run {{
  // table-based
  all t: Table | softno t.seat.tags
}} for {num_tables} Table, 5 int
"""

  tag_based = als + f"""
run {{
	// tag-based
	all t: Tag | softno seat.tags.t
}} for {num_tables} Table, 5 int
"""
  
  return sat, table_based, tag_based


def mode2(outpath, timeout=180):
  try:
    print("filename,table_maxsat,table_maxsat_part,tag_maxsat,tag_maxsat_part,sat,#inst")
    for tag in range(5, 10):
      for p in range(20, 36):
        min_p = 3
        max_p = 7
        
        if 20 <= p < 24:
          tab = 5
        elif 24 <= p < 28:
          tab = 6
        elif 28 <= p < 32:
          tab = 7
        elif 32 <= p < 36:
          tab = 8

        sat, table_based, tag_based = generate(tag, p, tag, tab, min_p, max_p)
        sat_filename = path.join(outpath, f"sat_{tag}_{p}_{tag}_{tab}_{min_p}_{max_p}.als")
        table_filename = path.join(outpath, f"table_{tag}_{p}_{tag}_{tab}_{min_p}_{max_p}.als")
        tag_filename = path.join(outpath, f"tag_{tag}_{p}_{tag}_{tab}_{min_p}_{max_p}.als")
        with open(sat_filename, "w") as f:
          f.write(sat)
        with open(table_filename, "w") as f:
          f.write(table_based)
        with open(tag_filename, "w") as f:
          f.write(tag_based)
        
        table_results = run_maxsat(table_filename, timeout=timeout)
        table_part_results = run_maxsat(table_filename, timeout=timeout, partition=True)

        tag_results = run_maxsat(tag_filename, timeout=timeout)
        tag_part_results = run_maxsat(tag_filename, timeout=timeout, partition=True)

        sat_results = run_sat(sat_filename, timeout=timeout)
        print(f"{tag}_{p}_{tag}_{tab}_{min_p}_{max_p},{table_results},{table_part_results},{tag_results},{tag_part_results},{sat_results}")
  except Exception as e:
    print(e)
  finally:
    shutil.rmtree(outpath)
    pass


def mode1(outpath, timeout=180, repeat=5):
  try:
    print("filename,table_maxsat,table_maxsat_part,tag_maxsat,tag_maxsat_part,sat,#inst")
    params = [
      (5, 20),
      (6, 24),
      (7, 28),
      (8, 32),
      (9, 36)
    ]
    for tag, p in params:
      for i in range(repeat):
        min_p = 3
        max_p = 7
        
        if 20 <= p < 24:
          tab = 5
        elif 24 <= p < 28:
          tab = 6
        elif 28 <= p < 32:
          tab = 7
        else:
          tab = 8

        sat, table_based, tag_based = generate(tag, p, tag, tab, min_p, max_p)
        sat_filename = path.join(outpath, f"sat_{tag}_{p}_{tag}_{tab}_{min_p}_{max_p}_{i}.als")
        table_filename = path.join(outpath, f"table_{tag}_{p}_{tag}_{tab}_{min_p}_{max_p}_{i}.als")
        tag_filename = path.join(outpath, f"tag_{tag}_{p}_{tag}_{tab}_{min_p}_{max_p}_{i}.als")
        with open(sat_filename, "w") as f:
          f.write(sat)
        with open(table_filename, "w") as f:
          f.write(table_based)
        with open(tag_filename, "w") as f:
          f.write(tag_based)
        
        table_results = run_maxsat(table_filename, timeout=timeout)
        table_part_results = run_maxsat(table_filename, timeout=timeout, partition=True)

        tag_results = run_maxsat(tag_filename, timeout=timeout)
        tag_part_results = run_maxsat(tag_filename, timeout=timeout, partition=True)

        sat_results = run_sat(sat_filename, timeout=timeout)
        print(f"{tag}_{p}_{tag}_{tab}_{min_p}_{max_p},{table_results},{table_part_results},{tag_results},{tag_part_results},{sat_results}")
  except Exception as e:
    print(e)


def mode0(outpath, timeout=180, repeat=5):
  try:
    params = [
      (7, 28, 6),
      (7, 30, 6),
      (8, 30, 7),
      (8, 32, 7),
      (9, 34, 8),
    ]
    min_p = 3
    max_p = 7
    for tag, p, tab in params:
      sat, table_based, tag_based = generate(tag, p, tag, tab, min_p, max_p)
      sat_filename = path.join(outpath, f"sat_{tag}_{p}_{tag}_{tab}_{min_p}_{max_p}.als")
      table_filename = path.join(outpath, f"table_{tag}_{p}_{tag}_{tab}_{min_p}_{max_p}.als")
      tag_filename = path.join(outpath, f"tag_{tag}_{p}_{tag}_{tab}_{min_p}_{max_p}.als")
      with open(sat_filename, "w") as f:
        f.write(sat)
      with open(table_filename, "w") as f:
        f.write(table_based)
      with open(tag_filename, "w") as f:
        f.write(tag_based)
      
      for _ in range(repeat):
        table_results = run_maxsat(table_filename, timeout=timeout)
        table_part_results = run_maxsat(table_filename, timeout=timeout, partition=True)

        tag_results = run_maxsat(tag_filename, timeout=timeout)
        tag_part_results = run_maxsat(tag_filename, timeout=timeout, partition=True)

        sat_results = run_sat(sat_filename, timeout=timeout)
        print(f"{tag}_{p}_{tag}_{tab}_{min_p}_{max_p},{table_results},{table_part_results},{tag_results},{tag_part_results},{sat_results}")
  except Exception as e:
    print(e)


if __name__ == "__main__":
  if len(sys.argv) == 2:
    print(
      "problem,table_trans,table_total,table_result," +
      "table_part_trans,table_part_total,table_part_result," +
      "tag_trans,tag_total,table_result," +
      "tag_part_trans,tag_part_total,table_part_result," +
      "sat_trans,sat_total,#inst")
    if sys.argv[1] == "-m=0":
      outpath = path.join(os.getcwd(), "mode0_out")
      if not path.exists(outpath):
        os.mkdir(outpath)
      mode0(outpath, timeout=600, repeat=5)
    elif sys.argv[1] == "-m=1":
      outpath = path.join(os.getcwd(), "mode1_out")
      if not path.exists(outpath):
        os.mkdir(outpath)
      mode1(outpath)
    elif sys.argv[1] == "-m=2":
      outpath = path.join(os.getcwd(), "mode2_out")
      if not path.exists(outpath):
        os.mkdir(outpath)
      mode2(outpath)
    else:
      print("Usage: benchmark.py -m=[0|1|2]")
  else:
    print("Usage: benchmark.py -m=[0|1|2]")

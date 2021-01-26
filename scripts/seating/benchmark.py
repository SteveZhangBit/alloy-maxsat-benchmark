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


if __name__ == "__main__":
  if len(sys.argv) < 3:
    print("Usage: benchmark.py <min_tag> <max_tag>")
    exit(1)

  print("filename,table_maxsat,table_maxsat_part,tag_maxsat,tag_maxsat_part,sat,#inst")

  outpath = path.join(os.getcwd(), "out")
  if not path.exists(outpath):
    os.mkdir(outpath)

  try:
    for tag in range(int(sys.argv[1]), int(sys.argv[2])):
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
        
        table_based_times = run_maxsat(table_filename, 180)
        tag_based_times = run_maxsat(tag_filename, 180)
        sat_time = run_sat(sat_filename, 180)
        print(f"{tag}_{p}_{tag}_{tab}_{min_p}_{max_p},{table_based_times},{tag_based_times},{sat_time}")
  finally:
    # shutil.rmtree(outpath)
    pass

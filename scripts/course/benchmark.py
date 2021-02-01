import subprocess
import os
from os import path
import shutil
import signal
import sys
import random
import numpy as np

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from util import run_sat, run_maxsat


def generate(num_courses, num_stu, max_core, max_interests):
  lec_types = [
    ["MonAM", "WedAM"],
    ["MonAM", "WedAM", "FriPM"],
    ["MonPM", "WedPM"],
    ["TueAM", "ThuAM"],
    ["TuePM", "TuePM"]
  ]

  courses = []
  students = []

  # generate courses
  for i in range(num_courses):
    courses.append(lec_types[np.random.randint(len(lec_types))])

  # generate students cores and interests
  for _ in range(num_stu):
    # generate cores
    cores = []
    tmp = list(range(num_courses))
    np.random.shuffle(tmp)

    t = set()
    for i in range(np.random.randint(max_core+1)):
      found = False
      for c in tmp[i:]:
        if set(courses[c]) & t == set():
          found = True
          cores.append(c)
          t = t | set(courses[c])
          break
      if not found:
        break
    
    # generate interests
    np.random.shuffle(tmp)
    if len(cores) > 1:
      interests = [cores[np.random.randint(len(cores))]]
    else:
      interests = []
      for c in tmp:
        if set(courses[c]) & t == set():
          interests.append(c)
          break
    for i in range(np.random.randint(max_interests)):
      interests.append(tmp[i+1])
    
    if len(cores) > 0:
      cores = " + ".join(["C" + str(i) for i in cores])
    else:
      cores = "none"
    interests = " + ".join(["C" + str(i) for i in interests])
    students.append((cores, interests))
  
  courses = list(map(lambda e: " + ".join(["C" + str(e[0]) + " -> " + l for l in e[1]]), enumerate(courses)))
  courses_str = " +\n    ".join(courses)
  student_str = "\n".join([
    f"one sig S{i} extends Student {{}} {{\n  core = {students[i][0]}\n  interests = {students[i][1]}\n}}"
    for i in range(len(students))
  ])
  
  als = f"""
abstract sig Day {{}}
one sig Mon, Tue, Wed, Thu, Fri extends Day {{}}

abstract sig Time {{}}
one sig AM, PM extends Time {{}}

abstract sig Course {{
  lectures: set Lecture
}}
one sig {",".join(["C" + str(i) for i in range(num_courses)])} extends Course {{}}

fact {{
  lectures = {courses_str}
}}

abstract sig Lecture {{
  day: one Day,
  time: one Time
}}
one sig MonAM, MonPM, TueAM, TuePM, WedAM, WedPM,
        ThuAM, ThuPM, FriAM, FriPM extends Lecture {{}}

fact {{
  day = MonAM -> Mon + MonPM -> Mon +
    TueAM -> Tue +TuePM -> Tue +
    WedAM -> Wed + WedPM -> Wed +
    ThuAM -> Thu + ThuPM -> Thu +
    FriAM -> Fri + FriPM -> Fri
  time = MonAM -> AM + MonPM -> PM +
    TueAM -> AM +TuePM -> PM +
    WedAM -> AM + WedPM -> PM +
    ThuAM -> AM + ThuPM -> PM +
    FriAM -> AM + FriPM -> PM
}}

abstract sig Student {{
  core: set Course,
  interests: set Course,
  courses: set Course
}}

{student_str}

pred conflict[c1, c2: Course] {{
  some l1, l2: Lecture {{
    l1 in c1.lectures
    l2 in c2.lectures
    l1.day = l2.day
    l1.time = l2.time
  }}
}}

pred validSchedule[courses: Student -> Course] {{
  all stu: Student {{
    #stu.courses > 2
    stu.core in stu.courses
    all disj c1, c2: stu.courses | not conflict[c1, c2]
  }}
}}

"""

  sat = als + "run AnySchedule { validSchedule[courses] }"
  maxsat = als + "run MaxInterests1 {\n  validSchedule[courses]\n  all stu: Student | maxsome stu.interests & stu.courses\n}"
  return sat, maxsat


def mode2(outpath, timeout=180):
  max_core = 3
  max_interests = 6
  try:
    for num_courses in range(10, 20):
      for num_stu in range(20, 30):
        sat, maxsat = generate(num_courses, num_stu, max_core, max_interests)

        sat_filename = path.join(outpath, f"sat_{num_courses}_{num_stu}_{max_core}_{max_interests}.als")
        with open(sat_filename, "w") as f:
          f.write(sat)

        maxsat_filename = path.join(outpath, f"maxsat_{num_courses}_{num_stu}_{max_core}_{max_interests}.als")
        with open(maxsat_filename, "w") as f:
          f.write(maxsat)
        
        maxsat_results = run_maxsat(maxsat_filename, timeout=timeout)
        maxsat_part_results = run_maxsat(maxsat_filename, timeout=timeout, partition=True)
        sat_results = run_sat(sat_filename, timeout=timeout)
        print(f"{num_courses}_{num_stu}_{max_core}_{max_interests},{maxsat_results},{maxsat_part_results},{sat_results}")
  except Exception as e:
    print(e)
  finally:
    shutil.rmtree(outpath)
    pass


def mode1(outpath, timeout=180, repeat=5):
  max_core = 3
  max_interests = 6
  params = [
    (12, 22),
    (14, 24),
    (16, 26),
    (18, 28)
  ]
  try:
    for num_courses, num_stu in params:
      for i in range(repeat):
        sat, maxsat = generate(num_courses, num_stu, max_core, max_interests)

        sat_filename = path.join(outpath, f"sat_{num_courses}_{num_stu}_{max_core}_{max_interests}_{i}.als")
        with open(sat_filename, "w") as f:
          f.write(sat)

        maxsat_filename = path.join(outpath, f"maxsat_{num_courses}_{num_stu}_{max_core}_{max_interests}_{i}.als")
        with open(maxsat_filename, "w") as f:
          f.write(maxsat)
        
        maxsat_results = run_maxsat(maxsat_filename, timeout=timeout)
        maxsat_part_results = run_maxsat(maxsat_filename, timeout=timeout, partition=True)
        sat_results = run_sat(sat_filename, timeout=timeout)
        print(f"{num_courses}_{num_stu}_{max_core}_{max_interests},{maxsat_results},{maxsat_part_results},{sat_results}")
  except Exception as e:
    print(e)


def mode0(outpath, timeout=180, repeat=5):
  max_core = 3
  max_interests = 6
  params = [
    (12, 22),
    (14, 24),
    (16, 26),
    (18, 28)
  ]
  try:
    for num_courses, num_stu in params:
      sat, maxsat = generate(num_courses, num_stu, max_core, max_interests)

      sat_filename = path.join(outpath, f"sat_{num_courses}_{num_stu}_{max_core}_{max_interests}.als")
      with open(sat_filename, "w") as f:
        f.write(sat)

      maxsat_filename = path.join(outpath, f"maxsat_{num_courses}_{num_stu}_{max_core}_{max_interests}.als")
      with open(maxsat_filename, "w") as f:
        f.write(maxsat)
      
      for _ in range(repeat):
        maxsat_results = run_maxsat(maxsat_filename, timeout=timeout)
        maxsat_part_results = run_maxsat(maxsat_filename, timeout=timeout, partition=True)
        sat_results = run_sat(sat_filename, timeout=timeout)
        print(f"{num_courses}_{num_stu}_{max_core}_{max_interests},{maxsat_results},{maxsat_part_results},{sat_results}")
  except Exception as e:
    print(e)


if __name__ == "__main__":
  if len(sys.argv) == 2:
    print("problem,maxsat_trans,maxsat_total,maxsat_result,maxsat_part_trans,maxsat_part_total,maxsat_part_result,sat_trans,sat_total,#inst")
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

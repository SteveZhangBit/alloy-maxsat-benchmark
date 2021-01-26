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
  days = ["Mon", "Tue", "Wed", "Thu", "Fri"]
  time = ["AM", "PM"]
  courses = []
  students = []

  # generate courses
  for i in range(num_courses):
    np.random.shuffle(days)
    lecs = days[:2]
    lecs = list(map(lambda x: x + time[int(np.random.randint(2))], lecs))
    courses.append(lecs)
    

  # generate students cores and interests
  for _ in range(num_stu):
    cores = [np.random.randint(num_courses)]
    tmp = list(range(num_courses))
    np.random.shuffle(tmp)

    for _ in range(1, max_core):
      t = set()
      for c in cores:
        t = t | set(courses[c])
      found = False
      for c in tmp:
        if set(courses[c]) & t == set():
          cores.append(c)
          found = True
          break
      if not found:
        break
    
    if len(cores) == 1:
      interests = list(np.random.randint(num_courses, size=np.random.randint(1, max_interests+1)))
    else:
      interests = list(np.random.randint(num_courses, size=np.random.randint(max_interests)))
      interests.append(cores[np.random.randint(len(cores))])
    
    cores = " + ".join(["C" + str(i) for i in cores])
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


if __name__ == "__main__":  
  outpath = path.join(os.getcwd(), "out")
  if not path.exists(outpath):
    os.mkdir(outpath)

  print("filename,maxsat,maxsat_part,sat,#inst")
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
        
        maxsat_result = run_maxsat(maxsat_filename, 180)
        sat_result = run_sat(sat_filename, 180)
        print(f"{num_courses}_{num_stu}_{max_core}_{max_interests},{maxsat_result},{sat_result}")
  except Exception as e:
    print(e)
  finally:
    # shutil.rmtree(outpath)
    pass

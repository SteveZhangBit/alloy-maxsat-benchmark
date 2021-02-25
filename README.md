# AlloyMax Benchmark
This package contains the benchmark for AlloyMax. Under the folder for each problem, the results from our experiments are stored in the csv files respectively.

## System Requirements
To run the benchmark, it requires Java version >= 1.8, and Python 3. The program has been tested under,
```
Java:
openjdk version "11.0.8" 2020-07-14
OpenJDK Runtime Environment (build 11.0.8+10-post-Ubuntu-0ubuntu120.04)
OpenJDK 64-Bit Server VM (build 11.0.8+10-post-Ubuntu-0ubuntu120.04, mixed mode, sharing)
```
```
Python 3.8.5
```

## Run AlloyMax
Unzip the package to a directory, run command
```
java -jar bin/org.alloytools.alloy.dist.jar
```
AlloyMax will run in GUI mode.

### Try the Course Scheduling Example
1. Open AlloyMax in GUI
    ```
    java -jar bin/org.alloytools.alloy.dist.jar
    ```

2. Open ```scripts/course/course_schedule.als```
3. Generate any valid schedule:

    3.1 Select: *Options -> Solver -> SAT4J*.

    3.2 Select: *Execute -> Run AnySchedule*.

    3.3 Click on the **Instance** on the right panel to open the visualizer.

    3.4 In the visualizer, select *Theme -> Load Theme -> course/course.thm* for simpler visualization.
4. Generate schedule that maximizes Alice's interests:

    4.1 Select: *Options -> Solver -> OpenWBO*.

        Note: Right now, OpenWBO only works on amd64 machines. Although SAT4JMax is cross-platform and works for Course problems, it does not work for some other problems (e.g., problems with softno).

    4.2 Select: *Execute -> Run MaxInterests1*.

    4.3 Repeat 3.3 and 3.4 for visualization.
5. Generate schedule with hard constraints on time preferences.

    5.1 Select: *Execute -> Run WithPrefer*. It should show UNSAT.
6. Generate schedule with soft time preferences.

    6.1 Uncomment Case 4.

    6.2 Select: *Execute -> Run WithSoftPrefer*.

        Note: comment it out if not using it, it may affect other problems.
7. Generate schedule with priorities on goals.

    7.1 Uncomment Case 5.

    7.2 Select: *Execute -> Run WithSoftPreferAndPrior*.

        Note: comment it out if not using it, it may affect other problems.
## Reproduce the results in the paper
### Course Scheduling
```
cd <path>/<to>/<package>/scripts/course

# run AlloyMax benchmark:
python benchmark.py -maxsat -maxsat_part -maxsat_part_auto -t=1800 -r=1 -m=models_20210203/

# run Alloy* benchmark:
python benchmark_alloy_star.py -t=1800 -r=1 -m=alloy_star_models/
```

### CheckMate
```
cd <path>/<to>/<package>/scripts/checkmate

# run AlloyMax benchmark:
python benchmark.py -maxsat -maxsat_part -maxsat_part_auto -t=1800 -r=1
```

### Degradation
```
cd <path>/<to>/<package>/scripts/degradation

# run AlloyMax benchmark:
python benchmark.py -maxsat -maxsat_part -maxsat_part_auto -t=1800 -r=1 -from_file
```
It's better to run this benchmark by using the ```from_file``` mode; otherwise, it may have memory problems.

### Wedding Seating
```
cd <path>/<to>/<package>/scripts/seating

# run AlloyMax benchmark:
python benchmark.py -maxsat -maxsat_part -maxsat_part_auto -t=1800 -r=1 -m=models_20210203/

# run Alloy* benchmark:
python benchmark_alloy_star.py -t=1800 -r=1 -m=alloy_star_models/
```

### Single Machine Scheduling
```
cd <path>/<to>/<package>/scripts/SMS

# run AlloyMax benchmark:
python benchmark.py -maxsat -maxsat_part -maxsat_part_auto -t=1800 -r=1 -m=models_20210203/

# run Alloy* benchmark:
python benchmark_alloy_star.py -t=1800 -r=1 -m=alloy_star_models/
```
*Known issue:* Although we set the same Alloy* solving options, the SMS problems can be solved from the GUI mode but in CLI mode they will have StackOverflow errors. Thus, we manually run the problems in GUI mode to collec the results.
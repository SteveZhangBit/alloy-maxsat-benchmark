# AlloyMax Benchmark
This is the reproduction package of the benchmarks used for the work *AlloyMax: Bringing Maximum Satisfaction to Relational Specifications* which will appear in FSE 2021. This package contains AlloyMax executable, the necessary libraries, the models used in the paper, and the scripts for running the benchmark.

## System Requirements
AlloyMax requires Java version >= 1.8. Although AlloyMax can run on both Windows and Linux machines, some of the back-end Sat/MaxSAT solvers can only run on Linux. Specifically, we use OpenWBO as the MaxSAT solver in our paper which can only run on Linux. **Therefore, we suggest using a Linux machine to reproduce our results.** Also, some models requires a large memory. **We suggest using a machine with at least 16GB memory.** We ran the benchmarks on a machine with 24GB memory.

In addition, the benchmark scripts require Python 3. The program has been tested under,
```
Java:
openjdk version "11.0.8" 2020-07-14
OpenJDK Runtime Environment (build 11.0.8+10-post-Ubuntu-0ubuntu120.04)
OpenJDK 64-Bit Server VM (build 11.0.8+10-post-Ubuntu-0ubuntu120.04, mixed mode, sharing)
```
```
Python 3.8.5
```

## Install Instruction
1. Clone this repository to your local machine.
```
cd <download directory>
git clone https://github.com/SteveZhangBit/alloy-maxsat-benchmark.git
```

2. Run AlloyMax
```
java -jar bin/org.alloytools.alloy.dist.jar
```
You should be able to see the AlloyMax GUI show up on the screen.

## Try out AlloyMax (Example in Section 2)
1. Open AlloyMax in GUI
    ```
    java -jar bin/org.alloytools.alloy.dist.jar
    ```

2. Open ```scripts/course/course_schedule.als```
3. Generate any valid schedule:

    3.1 Select: *Options -> Solver -> SAT4J or OpenWBO*.

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

## Reproduce the benchmark results in the paper (Section 6)
We can use the ```benchmark.py``` script to run the benchmark. The script allows different options to enable different solving mode. Run ```python benchmark.py``` should see:
```
Usage: benchmark.py
	-sat			Enumerate all solutions by using SAT
	-maxsat			Find one optimal solution
	-maxsat_all		Find all optimal solutions
	-maxsat_part		Find one optimal solution by using Max-SAT with user partitioning
	-maxsat_part_auto	Find one optimal solution by using auto partitioning
	-t=<timeout>
	-r=<repeat>
	-m=<model path>
	-from_file		Generate the CNF/WCNF file and then call the solver
```

*Note: Alloy generates tmp files to solve problems. You could clean your /tmp directory after running the benchmark.*

### Course Scheduling (Section 6.2.1)
```
cd <path>/<to>/<package>/scripts/course

# run AlloyMax benchmark:
python benchmark.py -maxsat -maxsat_part -maxsat_part_auto -t=1800 -r=1 -m=models_20210203/

# run Alloy* benchmark:
python benchmark_alloy_star.py -t=1800 -r=1 -m=alloy_star_models/
```

### CheckMate (Section 6.2.2)
```
cd <path>/<to>/<package>/scripts/checkmate

# run AlloyMax benchmark:
python benchmark.py -maxsat -maxsat_part -maxsat_part_auto -t=1800 -r=1
```

### Degradation (Section 6.2.3)
```
cd <path>/<to>/<package>/scripts/degradation

# run AlloyMax benchmark:
python benchmark.py -maxsat -maxsat_part -maxsat_part_auto -t=1800 -r=1 -from_file
```
It's better to run this benchmark by using the ```from_file``` mode; otherwise, it may have memory problems.

### Wedding Seating (Section 6.2.4)
```
cd <path>/<to>/<package>/scripts/seating

# run AlloyMax benchmark:
python benchmark.py -maxsat -maxsat_part -maxsat_part_auto -t=1800 -r=1 -m=models_20210203/

# run Alloy* benchmark:
python benchmark_alloy_star.py -t=1800 -r=1 -m=alloy_star_models/
```

### Single Machine Scheduling (Section 6.2.5)
```
cd <path>/<to>/<package>/scripts/SMS

# run AlloyMax benchmark:
python benchmark.py -maxsat -maxsat_part -maxsat_part_auto -t=1800 -r=1 -m=models_20210203/

# run Alloy* benchmark:
python benchmark_alloy_star.py -t=1800 -r=1 -m=alloy_star_models/
```
*Known issue:* Although we set the same Alloy* solving options, the SMS problems can be solved from the GUI mode but in CLI mode they will have StackOverflow errors. Thus, we manually run the problems in GUI mode to collect the results.

## AlloyMax Source Code
You can also access the source code of AlloyMax from: https://github.com/SteveZhangBit/org.alloytools.alloy/tree/maxsat

This repository is a fork from the original Alloy project. Our modification is on branch ```maxsat```. You can follow the build instruction for Alloy to build AlloyMax.
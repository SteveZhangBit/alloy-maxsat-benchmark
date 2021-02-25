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
#!/bin/bash

cd course
python benchmark.py -maxsat -t=1800 -r=1 -m=models_20210203 > one_result_maxsat.csv
python benchmark.py -maxsat_part_auto -t=1800 -r=1 -m=models_20210203 > one_result_maxsat_part_auto.csv

cd ../checkmate
python benchmark.py -maxsat -t=1800 -r=1 > one_result_maxsat.csv
python benchmark.py -maxsat_part_auto -t=1800 -r=1 > one_result_maxsat_part_auto.csv

cd ../seating
python benchmark.py -maxsat -t=1800 -r=1 -m=models_20210203 > one_result_maxsat.csv
python benchmark.py -maxsat_part_auto -t=1800 -r=1 -m=models_20210203 > one_result_maxsat_part_auto.csv

cd ../SMS
python benchmark.py -maxsat -t=1800 -r=1 -m=models_20210203 > one_result_maxsat.csv
python benchmark.py -maxsat_part_auto -t=1800 -r=1 -m=models_20210203 > one_result_maxsat_part_auto.csv

cd ../degradation
python benchmark.py -maxsat -t=1800 -r=1 -from_file > one_result_maxsat.csv
python benchmark.py -maxsat_part_auto -t=1800 -r=1 -from_file > one_result_maxsat_part_auto.csv

# Run again
cd ../course
python benchmark.py -maxsat -t=1800 -r=4 -m=models_20210203 > new_result_maxsat.csv
python benchmark.py -maxsat_part_auto -t=1800 -r=4 -m=models_20210203 > new_result_maxsat_part_auto.csv

cd ../checkmate
python benchmark.py -maxsat -t=1800 -r=4 > new_result_maxsat.csv
python benchmark.py -maxsat_part_auto -t=1800 -r=4 > new_result_maxsat_part_auto.csv

cd ../seating
python benchmark.py -maxsat -t=1800 -r=4 -m=models_20210203 > new_result_maxsat.csv
python benchmark.py -maxsat_part_auto -t=1800 -r=4 -m=models_20210203 > new_result_maxsat_part_auto.csv

cd ../SMS
python benchmark.py -maxsat -t=1800 -r=4 -m=models_20210203 > new_result_maxsat.csv
python benchmark.py -maxsat_part_auto -t=1800 -r=4 -m=models_20210203 > new_result_maxsat_part_auto.csv

cd ../degradation
python benchmark.py -maxsat -t=1800 -r=4 -from_file > new_result_maxsat.csv
python benchmark.py -maxsat_part_auto -t=1800 -r=4 -from_file > new_result_maxsat_part_auto.csv

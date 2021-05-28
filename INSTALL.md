# Install Instruction
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
You can follow the instruction below to run the course scheduling problem in Section 2 of the paper.

1. Open AlloyMax in GUI
    ```
    java -jar bin/org.alloytools.alloy.dist.jar
    ```

2. Open ```scripts/course/course_schedule.als```
3. Generate any valid schedule:

    3.1 Select: *Options -> Solver -> SAT4J*.

    3.2 Select: *Execute -> Run AnySchedule*.

    3.3 Click on the **Instance** on the right panel to open the visualizer.

    3.4 In the visualizer, select *Theme -> Load Theme -> course/course.thm* for simpler visualization. Then, you should see a similar model as it in Figure 2 of the paper.

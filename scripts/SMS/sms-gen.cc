#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <vector>
#include <fstream>

using namespace std;

typedef struct fragment {
  int release;
  int processing;
  int deadline;
} fragment_t;

typedef struct task {
  fragment_t* fragments;
  int nFragments;
  int release;
  int processing;
  int deadline;
  int* dependencies;
  int nDependencies;
  int read;
} task_t;


// Task Data
task_t* _tasks;
int _nTasks;

// Aux Data
int _maxDeadline = 0;
int _maxProcessing = 0;
int _maxFragments = 0;
int _maxSlack = 1;
int _maxDependencies = 0;
int _seed = 0;

// Show usage
void printUsage() {
  printf("sms-gen #Tasks MaxDeadline MaxProcessing MaxFragments Slack MaxDependencies seed\n");
  printf("\t #Tasks: number of tasks to schedule\n");
  printf("\t MaxDeadline: definition of timeframe\n");  
  printf("\t MaxProcessing: maximum task duration\n");  
  printf("\t MaxFragments: maximum number of fragments per task\n");  
  printf("\t MaxSlack: maximum value of slack in task\n");
  printf("\t MaxDependencies: maximum number of dependencies between tasks.\n");
  printf("\t seed: random seed initialization.\n");
}


// Generate an integer between min and max
int genInt(int m, int M) {
  int v = rand() % (M-m+1);
  v += m;
  return v;
}


// Generate Tasks
void generateTasks() {
  int min_release = _maxDeadline;
  _tasks = new task_t[_nTasks];
  for (int i = 0; i < _nTasks; i++) {
    _tasks[i].release = genInt(0, _maxDeadline);
    if (_tasks[i].release < min_release) min_release = _tasks[i].release;
    _tasks[i].processing = genInt(1, _maxProcessing);
    _tasks[i].deadline = _tasks[i].release + genInt(1, _maxSlack) * _tasks[i].processing;
    _tasks[i].nFragments = genInt(1, _maxFragments);
    if (_tasks[i].nFragments > _tasks[i].processing) _tasks[i].nFragments = _tasks[i].processing;
    _tasks[i].fragments = new fragment_t[_tasks[i].nFragments];
    for (int j = 0; j < _tasks[i].nFragments; j++) {
      _tasks[i].fragments[j].release = _tasks[i].release;
      _tasks[i].fragments[j].processing = 1;
      _tasks[i].fragments[j].deadline = _tasks[i].deadline;
    }
    int p = _tasks[i].nFragments;
    while (p < _tasks[i].processing) {
      int f = genInt(0, _tasks[i].nFragments-1);
      _tasks[i].fragments[f].processing++;
      p++;
    }
    _tasks[i].nDependencies = 0;
    _tasks[i].dependencies = new int[_maxDependencies];
  }
  
  // Generate dependencies
  int dependencies = 0;
  for (int d = 0; d < _maxDependencies*4; d++) {
    int t1 = genInt(0, _nTasks-1);
    int t2 = genInt(0, _nTasks-1);
    while (t1 == t2) {
      t2 = genInt(0, _nTasks-1);
    }
    // Check if t1 and t2 are compatible
    // t1 before t2
    if (_tasks[t1].release + _tasks[t1].processing < _tasks[t2].deadline - _tasks[t2].processing) {
      int t2_depend = _tasks[t2].nDependencies;
      int exists = 0;
      for (int k = 0; k < t2_depend; k++) {
	if (_tasks[t2].dependencies[k] == t1+1) { exists = 1; break; }
      }
      if (exists == 0) {
	_tasks[t2].dependencies[t2_depend] = t1+1;
	_tasks[t2].nDependencies++;
	dependencies++;
      }
    }
    // t2 before t1
    else if (_tasks[t2].release + _tasks[t2].processing < _tasks[t1].deadline - _tasks[t1].processing) {
      int t1_depend = _tasks[t1].nDependencies;
      int exists = 0;
      for (int k = 0; k < t1_depend; k++) {
	if (_tasks[t1].dependencies[k] == t2+1) { exists = 1; break; }
      }
      if (exists == 0) {
	_tasks[t1].dependencies[t1_depend] = t2+1;
	_tasks[t1].nDependencies++;
	dependencies++;
      }
    }
    if (dependencies == _maxDependencies) break;
  }
  
  // Make sure the timeline starts at 0
  for (int i = 0; i < _nTasks; i++) {
    _tasks[i].release -= min_release;
    _tasks[i].deadline -= min_release;
  }
}


// Output Tasks
void outputTasks() {
  printf("%d\n", _nTasks);
  for (int i = 0; i < _nTasks; i++) {
    printf("%d %d %d %d", _tasks[i].release, _tasks[i].processing, _tasks[i].deadline, _tasks[i].nFragments);
    for (int j = 0; j < _tasks[i].nFragments; j++) {
      printf(" %d", _tasks[i].fragments[j].processing);
    }
    printf("\n");
  }
  for (int i = 0; i < _nTasks; i++) {
    printf("%d", _tasks[i].nDependencies);
    for (int j = 0; j < _tasks[i].nDependencies; j++) {
      printf(" %d", _tasks[i].dependencies[j]);
    }
    printf("\n");
  }
}


// Main funcion
int main(int argc, char *argv[]) {
  
  if (argc != 8) {
    printf("Wrong number of arguments. Check usage info.\n\n");
    printUsage();
    exit(0);
  }
  
  sscanf(argv[1], "%d", &_nTasks);
  sscanf(argv[2], "%d", &_maxDeadline);
  sscanf(argv[3], "%d", &_maxProcessing);
  sscanf(argv[4], "%d", &_maxFragments);
  sscanf(argv[5], "%d", &_maxSlack);
  sscanf(argv[6], "%d", &_maxDependencies);
  sscanf(argv[7], "%d", &_seed);
  
  // Seed init
  srand(_seed);
  
  generateTasks();

  outputTasks();
  
  return 0;
}

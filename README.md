# Salesman Heuristics - GTwA Project 1

### Setup

Create a Python virtualenv with interpreter version 2.7 or later on your UNIX system. Activate the virtualenv with `source bin/activate`, and then create a new folder called `project`. Navigate into this folder, and clone this repository.

### Dependency Installation

If you are on a Linux system, you may need to run `apt-get install libfreetype6-dev python-dev tcl-dev tk-dev
 python-matplotlib`. Install all dependencies by running `pip install -r requirements.txt`.  

### Running
`python salesman.py [-h] `

`[--no-animate] [--bruteforce] [--random] [cities]`

# Examples:
To bruteforce a graph on five cities `python salesman.py --no-animate --bruteforce 5`
To display an animate heuristic graph on ten cities `python salesman.py 10`
To display a static heuristic graph on ten random vertices `python salesman.py --random 10`

### Output

All output should go to ./output until we find a better way to display our results.

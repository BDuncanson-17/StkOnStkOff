==================================
StkOnStkOff
==================================

Stack On Stack Off is a Python tool that automates the creation and deletion of AWS CloudFormation stacks.

Features
========

* Create CloudFormation stacks from local templates
* Allow users to select:
    * Set a stack creation/deletion order
    * Sequential none overlapping creation/deletion stacks
    * Name stacks from the terminal
* Easily manage your infrastructure

Requirements
============

* Python 3.7 - Python 3.10
* Boto (Replace with actual dependencies)
* cfn-lint (Replace with actual dependencies)


Installation
============

Installation
------------

To install and set up the `stkonstkoff` project, follow these steps:

1. Create and activate a virtual environment:

   .. code-block:: bash

      python -m venv .venv
      source .venv/bin/activate

2. Clone the repository:

   .. code-block:: bash

      git clone https://www.github.com/bduncanson-17/stkonstkoff
      cd stkonstkoff

3. Install the project dependencies:

   .. code-block:: bash

      python -m pip install -r setup.cnf

4. Install the project in editable mode:

   .. code-block:: bash

      python -m pip install -e .

   This will install the project in editable mode, allowing you to make changes to the code without reinstallation.


Usage
=====

To Do

Contributing
============

To Do

License
=======

StkOnStkOff is released under the MIT LICENSES
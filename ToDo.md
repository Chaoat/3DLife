Roots
=====
1. We're using python for GUI and Simulation
2. We're using c++ for the visualisation
3. For interface we're using PyQt

Features
========
1. Ability to have different rules. Creating own rules would be cool too.
2. I think there are some rules that have non binary states, as in they can be alive, unhealthy, then dead, or any number of states inbetween.
3. Multiple time dimensions?
4. Simple interface. I think there already exists tools that do at least some of the new things we want to try out, but they're all extremely impenetrable.
5. Variable simulation speed
6. Variable number of dimensions. This is the key thing that seperates us from already existing life implementations.
7. Variable number of unique states for each cell, conveyed by different colours.
8. Handle startup sequence. In order for everything to talk, first we have to start the python, have it wait for the c++ to be ready, and only then import the controls module.   

Done
====
C++
---
* Implement orbital camera and camera controls
* Use relative paths to find python files
* Retrieve state and dimensions from python
* Ability to colour each cell
* Variable number of dimensions.

http://yyc.solvcon.net/writing/2016/resource/
http://www.stuffaboutcode.com/2013/08/shared-memory-c-python-ipc.html
https://stackoverflow.com/questions/31028012/access-a-boostinterprocess-shared-memory-block-from-python-with-ctypes
https://www.codeproject.com/Articles/11843/Embedding-Python-in-C-C-Part-II
https://github.com/teeks99/py_boost_shmem
https://blog.schmichael.com/2011/05/15/sharing-python-data-between-processes-using-mmap/
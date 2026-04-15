```
multi agent python app builder

problem statement:
To build a multi agent system that codes python apps

agents:

planner -> plans the steps
worker -> outputs python code for each of the steps
creator -> creates files with code

problems:

-creating very complex code even if i have given minimal
-no proper structure/architecture
-files are not getting created properly in the folders
-very slow(3m 42s for task manager)


improvements that can be made:

-add code correction if it is wrong before creator
-add feedback before creating structure
-add feedback if not satisfied with code
-show structure to user before creation
-can also specify path for creation
-can ask for more requiremnts for the user and when satisfied can start
-can add parallel workers 
-can add tester node to test code and retry logic if code is not adequate
```
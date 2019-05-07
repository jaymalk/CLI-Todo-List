## Todo List Tool

**A simple python based tool to handle todo lists on terminal**
<br>

*Outline*
 - [Libraries](#dependencies)
 - [Specifications](#python-definition)
 - [Shots](#screenhots)

### Dependencies
    Following python libraries were used.
- *sqlite3*
- *argparse*
- *datetime*
- *sys*


### Python Definition
```usage: [-h] [-all] [-new] [-rm] [-more] [-edit] [-lmt LIMIT] [-sort]```

*For performing list operations from command line.*

*Optional arguments:*
 -  ```-all```        *Show the list.*
 -  ```-new```        *New entry*
 -  ```-rm```         *Delete entry*
 -  ```-more```       *Show task detail*
 -  ```-edit```       *Edit task detail*
 -  ```-lmt LIMIT```  *Limiting the display of tasks*
 -  ```-sort```       *Display sorted by deadline*


#### Screenshots

<p align="center">
        <img src = "https://github.com/jaymalk/CLI-Todo-List/blob/master/readme_files/basic.png">
</p>
<p align="center">
        <img src = "https://github.com/jaymalk/CLI-Todo-List/blob/master/readme_files/detail.png">
</p>
<p align="center">
        <img src = "https://github.com/jaymalk/CLI-Todo-List/blob/master/readme_files/sorted.png">
</p>
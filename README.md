# RavenDirBuster
RavenBuster is a directory and file busting tool that has functionality to find directories and files using dictionary attack technique. In order to use this tool, you will be needed a dictionary or a wordlist file. 


Be careful using the tool in multi-threaded mode since it can be treated as DoS attack and your IP can be blocked by the cloud host. 


This tools is developed by Nitin Choudhury, Founder and CEO of CyberRaven Securities.

## Requirements
This is a python based file. So, to run this file you will require a python environment.

## Set-Up
Step-1: Download the zip file or clone

`git clone https://github.com/nitin293/RavenDirBuster/`

Step-2: Run the file

```
cd RavenDirBuster/
python3 ravenDirBuster.py --help
```

![img](./assets/img-0.png)

## Uses

* Run using multi-threading

`python3 ravenDirBuster.py -u https://google.com --thread 100`

![img](./assets/img-1.png)


* Run in recursive mode to find nested directories

> can't be run in multi-threaded mode

`python3 ravenDirBuster.py -u https://google.com --recursion True`

![img](./assets/img-2.png)


* Search for files with specific extension

> Can be run with multi-threading

`python3 ravenDirBuster.py -u https://google.com -e html,txt`

![img](./assets/img-3.png)


* Run by filtering response code

> can be run in multi-threaded mode

![img](./assets/img-4.png)

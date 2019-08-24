**[Installation](#setup-instructions)** |
**[How to use](#how-to-use)** |
**[How to write tests](write_test.md)**|
**[Code](https://github.com/Divya063/TestingFramework)**

# Google Summer of Code 2019

# [Testing Framework for Jupyter notebooks](https://summerofcode.withgoogle.com/projects/#5216539194687488)

<center>
<table>
<tr>
<td><a href="https://summerofcode.withgoogle.com/projects/#5216539194687488"><img src="https://user-images.githubusercontent.com/6822941/29750351-e95e7b1c-8b5b-11e7-9f6b-b25b69f7353a.png"/></a></td>
<td><a href="http://hepsoftwarefoundation.org/"><img src="https://user-images.githubusercontent.com/6822941/29750350-e956b512-8b5b-11e7-9e34-4e3a5be9d37f.png"/></a></td>
<td><a href="https://swan.web.cern.ch/"><img src="https://avatars0.githubusercontent.com/u/38285709?s=200&v=4"/></a></td>
</tr>
</table>
</center>

## Mentors
- Enrico Bocchi
- Diogo Castro
- João Vicente
- Jakub Moscicki
- Enric Tejedor

## Introduction

SWAN (Service for Web-based ANalysis) is a cloud data analysis service developed and powered by CERN that provides Jupyter notebooks on demand. It is based on Jupyter upstream technology but it is deeply integrated with CERN-specific services, e.g., EOS which provides storage to SWAN , CVMFS which is used to retrieve software on the fly. Jupyter notebooks, despite being easily accessible from an intuitive web-based interface, are a complex environment, especially when used together with JupyterHub, custom extensions, external storage backends and computational clusters. This project aims at creating a testing framework for both upstream Jupyter components and SWAN-specific components which will allow the addition of new tests to cover new features of the SWAN service and will be able to run synthetic tests. The testing framework is self contained and  includes functional tests as well as performance tests.

This testing framework covers the following components:

Upstream Components :
1. configurable-http-proxy
2. [JupyterHub API](#jupyterhub-api)
3. [SQLite database managed by JupyterHub](#sqlite-database)
4. [SWAN docker containers](#container)

CERN-specific components :
1. [The EOS filesystem](#storage)
2. [The CVMFS repositories](#cvmfs)


## Setup Instructions

- This project assumes a [SWAN](https://swan.web.cern.ch/) or [ScienceBox](https://github.com/cernbox/uboxed) setup. ScienceBox contains SWAN and all the other CERN-specific services (i.e., EOS, CERNBox, CVMFS). To install required dependencies:

```bash
git clone https://github.com/Divya063/TestingFramework.git
cd TestingFramework
pip3 install -r requirements.txt
```

## How to use

There are two testing modes:
 - From the host machine (default)
 - From containers (sciencebox) - To run the test from user container use the flag `-u` and pass the 
 session name as `--session {name}`, e.g- `--session user2`
 
 
To run tests from host machine use the command - `python3 run.py --configfile [path of yaml file]`, while running this command it is assumed that all the parameters (required to run the tests) are provided in the [test.yaml]() file or in some cases([JupyterHub API](#warning)) necessary configuration has already been done. <br>

### Storage

- To run the test from user container use the command given below (there is no need to provide path argument as it will
be already set in test.yaml file.)<br>
`python3 run.py -u --session user2 --test storage --configfile test.yaml`

**Parameters**
```yaml
    mount_sanity:
      timeout: 8
      mountpoints: ['user/u/user2/']
    mount:
      user_mode : 'sciencebox'
    write:
      fileSize: 1M
      filepath: "eos/user/u/user2/0.txt"
    delete:
      filepath: "eos/user/u/user2/0.txt"
    exists:
      filepath: "eos/user/u/user2/0.txt"
    throughput: 
      fileNumber: 10
      fileSize: 1M
      filepath: "eos/user/u/user2/"
    checksum:
      fileNumber: 10
      fileSize: 1M
      filepath: "eos/user/u/user2/"
```
1. mount_sanity:
    - Test file : test_mount_sanity.py
    - Use case : Given a list of mount points checks if a mount point is hanging
    - To run this test explicitly use -  `python3 test_mount_sanity.py --timeout 5 --mount_points user user/u`

2. mount:
    - Test file : test_mount.py
    - Use case : Checks if eos is mounted on host and sciencebox
    - There are two testing modes:
      - "host"
      - "sciencebox"
    -  To run this test explicitly use - `python3 test_mount.py --mode host`
    
3. throughput:
    - Test file : test_throughput.py
    - Use case : Benchmark read-write performance and compute the read and write throughput.
    - To run this test explicity use - `python3 test_throughput.py --num 10 --file-size 1M --dest eos/user/u/user2`
    
4. checksum : 
    - Test file : test_checksum.py
    - Use case : Calculates the checksum
    - To run this test explicity use - `python3 test_checksum.py --num 10 --file-size 1M --dest eos/user/u/user2`

### CVMFS

- To run the test from user container use the command given below.<br>
`python3 run.py -u --session user2 --test CVMFS --configfile test.yaml`

**Parameters**

```yaml
cvmfs:
    mount:
      repoName: 'sft.cern.ch'
      repoPath: 'cvmfs/sft.cern.ch/'
    ttfb:
      repoPath: 'cvmfs/sft.cern.ch/'
      filePath: 'cvmfs/sft.cern.ch/lcg/lastUpdate'
    throughput:
      num: 2 #Number of packages you want to read
      repoPath: 'cvmfs/sft.cern.ch/'
      filePath: 'cvmfs/sft.cern.ch/lcg/releases/'
```
1. mount : 
    - Test file : test_mount.py
    - Use case : Checks if cvmfs folder is mounted or not
    - To run this test explicity use - `python3 test_mount.py --repo sft.cern.ch --path cvmfs/sft.cern.ch/`
2. ttfb:
    - Test file : test_ttfb.py
    - Use case : Evaluates the time needed to get the first byte (TTFB) of a file known to exist (lastUpdate).
    - To run this test explicity use - `python3 test_ttfb.py ---repo sft.cern.ch --path cvmfs/sft.cern.ch/lcg/lastUpdate`
    
3. throughput:
    - Test file : test_throughput.py
    - Use case : Benchmark performance when reading from the repository and compute the read throughput.
    - To run this test explicity use - `python3 test_throughput.py --num 2 --repo_path cvmfs/sft.cern.ch --path cvmfs/sft.cern.ch/lcg/releases/`

### Jupyterhub API

- To run the tests from jupyterhub container use `python3 run.py -u --session {session-name} --test jupyterhub-api --configfile test.yaml`.
e.g - `python3 run.py -u --session user2 --test jupyterhub-api --configfile test.yaml`

1. Parameters

Parameters for the test is present in test.yaml which is as follows:

```yaml
     jupyterhub_api:
    check_api:
      hostname: 'localhost'
      port: '443'
      token: ""
      base_path: ""
      verify : False
    token:
      hostname: 'localhost'
      port: '443'
      token: ""
      users: ['user2']
      base_path: ""
      verify: False
    create_session:
      hostname: 'localhost'
      port: '443'
      token: 'b39639d589c44a2294b3dd1164607287'
      users: ['user2']
      base_path: ""
      params:
        TLS: False
        LCG-rel: "LCG_95a"
        platform: "x86_64-centos7-gcc7-opt"
        scriptenv: "none"
        ncores: 2
        memory: 8589934592
        spark-cluster: "none"
      delay: 30 #Max
      verify: False
    check_session:
      hostname: 'localhost'
      port: '443'
      token: ""
      users: ['user2']
      base_path: ""
      verify: False
    stop_session:
      hostname: 'localhost'
      port: '443'
      token: ''
      users: ['user2']
      base_path: ""
      verify: False
```
1. **check_api** 
    - Test file : test_check_api.py"
    - Use case :  Checks hub's sanity by making a GET request to "https://localhost:443/hub/api/".
On successful execution response code should be *200*.
    - To run this test explicity use - `python3 test_check_api.py --token " " --port 443 --base_path ""`

2. **token**
    - Test file : test_token.py"
    - Use case :  Checks token validity by making a GET request to "https://localhost:443/hub/api/users/user{}".
On successful execution response code should be *200*.
    - To run this test explicity use - `python3 test_token.py --port 443 --token " " --users user1 --base_path ""`

2. **create_session** 
   - Test file : test_create_session.py
   - Use case : Checks if session can be created successfully or not.
   - parameters : 
     - params : This data needs to be passed to create a user container
     - timedelay : In the process of creating sessions, first the required user's server is requested which is  validated by the response code *202*, a server is created consequently, which needs to repond within 30s, otherwise the server
      will be obliterated. The wait time is maximum 30s, if the server didn't respond within stipulated time, response code *500* will be received.<br>
      Example :    
      `TimeoutError: Server at http://172.18.0.15:8888/user/user0/ didn't respond in 30 seconds`
    - To run the test explicitly use following command:
       `python3 test_create_session.py --port 443 --token " " --users user2  --json '{"LCG-rel": "LCG_95a", "platform": "x86_64-centos7-gcc7-opt", "scriptenv": "none", "ncores": 2, "memory": 8589934592, "spark-cluster": "none"}' --delay 30 --base_path ""`

   ---
 ### warning
   Before creating servers/sessions make sure -
   
   - You generate the token by running `jupyterhub token dummy_admin`, add the token inside jupyterhub_config.py
   file as `c.JupyterHub.service_tokens = {'dummy_admin' : '<token_value>'}` and restart the jupyterhub process with `supervisorctl restart jupyterhub`.
   Also add the token to "token" field present in the yaml file.
   
   - And you have created users as each server is created for one particular user. <br>
   
       - Using curl :
       `curl -XPOST -v -k https://localhost:443/hub/api/users/user2 -H "Authorization: token {token from yaml file}"`
       - Python code :
       ```python
           def check_create_users(self):
            """
            Inside container
            port = 443
            Ouside container
            port = 8443
            """
            self.log.write("info", "creating users..")
            print(self.users)
            for user in self.users:
                global r
                try:
                    r = self.session.create_users(user)
                except Exception as err:
                    self.exit |= 1
                    self.log.write("error", str(err))
                    self.log.write("error", str(r))
                else:
                    if r.status_code == 201:
                        self.log.write("info", user + " successfully created")
                    else:
                        self.log.write("error", (r.content).decode('utf-8'))
                        self.exit |= 1
            self.log.write("info", "Exit code " + str(self.exit))
            return self.exit
     ```
       ---
3. **check_session**
    - Test file : test_check_session.py
    - Use case : Checks if a session is running or not
    - To run this test explicitly use -
        - For single user - `python3 test_check_session.py --port 443 --token " " --users user1 --base_path ""`
        - For multiple users - `python3 test_check_session.py --port 443 --token " " --users user0 user1 user2 --base_path ""`

4. **stop_session**

     - Test file : test_stop_session.py
     - Use case : Checks if a session  can be stopped or not
     - To run this test explicitly use -
        - For single user - `python3 test_stop_session.py --port 443 --token " " --users user1 --base_path ""`
        - For multiple users - `python3 test_stop_session.py --port 443 --token " " --users user0 user1 user2 --base_path ""`

### sqlite database

- This test checks the consistency of the sqlite database present inside `srv/jupyterhub/` as jupyterhub.sqlite.
- To run this test use 
`python3 run.py -u --session user2 --test database --configfile test.yaml`
Parameters:

```yaml
database:
    token:
      path: "jupyterhub.sqlite"
      user: "user2"
      mode: "active" #active mode
      table_name: "api_tokens"
    servers:
      path: "jupyterhub.sqlite"
      user: "user2"
      mode: "active" #active mode
      table_name: "servers"
    spawners:
      path: "jupyterhub.sqlite"
      user: "user2"
      mode: "active" #active mode
      table_name: "spawners"
```
Two modes are there:
- active mode - When the server is active
- delete mode - When the server is removed or deleted

1. **token**
     - Test file : test_token.py
     - Use case : Checks the status of "token" table when a session is created or removed.
     - To run this test explicitly use - 
       `python3 test_token.py --path jupyterhub.sqlite -d --user user2 --table api_tokens`

2. **servers**

     - Test file : test_servers.py
     - Use case : Checks the status of "servers" table when a session is created or removed.
     - To run this test explicitly use - 
       `python3 test_servers.py --path jupyterhub.sqlite -d --user user2 --table servers`
       
3. **spawners**

    - Test file : test_spawners.py
    - Use case : Checks the status of "spawners" table when a session is created or removed.
    - To run this test explicitly use - 
       `python3 test_spawners.py --path jupyterhub.sqlite -d --user user2 --table spawners`     

       
### Container

- To run this test use `python3 run.py --configfile test.yaml` (this test is not meant to be run from the containers)

Parameters:

```yaml
user_docker:
    docker:
      container_name: 'jupyter-user2'
      timeout: 5
```
Checks if a container is healthy or not.  

## Future Work
   - Pending Work
      + [Filed issues](https://github.com/Divya063/TestingFramework/issues)
      + Implement healthchecking mechanism similar to liveliness-probes and readiness-probes
      
### Student

***Divya Rani***

- **Email ID**: [ranidivya063@gmail.com](mailto:ranidivya063@gmail.com)
- **Linkedin Profile**: [https://linkedin.com/in/divya-rani-23924481/](https://linkedin.com/in/divya-rani-23924481/)


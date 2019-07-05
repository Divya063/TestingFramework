Jupyterhub API tests

To run all the tests use `python3 run.py --test jupyterhub-api --configfile test.yaml`

1. Parameters

Parameters for the test is present in test.yaml which is as follows:

```yaml
     jupyterhub_api:
        check_api:
          port: '443'
          TLS : False
        create_session:
          port: '443'
          users: ['user2']
          token: ''
          params:
            TLS: False
            LCG-rel: "LCG_95a"
            platform: "x86_64-centos7-gcc7-opt"
            scriptenv: "none"
            ncores: 2
            memory: 8589934592
            spark-cluster: "none"
          TLS: False
          timedelay: 30 #Max
          path: '/srv/jupyterhub'
        check_session:
          port: '443'
          users: ['user2']
          TLS: False
        stop_session:
          port: '443'
          users: ['user2']
          TLS: False

```
1. **check_api** 
    - Test file : test_check_api.py"
    - Use case :  check hub's sanity by making a GET request to "https://localhost:443/hub/api/".
On successful execution response code should be 200.
    - To run this test explicity use - `python3 test_check_api.py --port 443`
    
2. **create_session** 
   - Test file : test_create_session.py
   - Use case : creates a token and updates the token field in test.yaml file, 
   checks if session can be created successfully or not.
   - parameters : 
     - params : This data needs to be passed to create a user container
     - timedelay : In the process of creating sesions, first the required user's server is requested which is  validated by the response code 202, a server is created consequently, which needs to repond within 30s, otherwise the server
      will be obliterated. The wait time is maximum 30s, if the server didn't respond within stipulated time, response code 500 will be received.<br>
      Example :    
      `TimeoutError: Server at http://172.18.0.15:8888/user/user0/ didn't respond in 30 seconds`
    - To run the test explicitly use following command:
       `  python3 test_create_session.py --port 443 --users user2 --path /srv/jupyterhub --json '{"LCG-rel": "LCG_95a", "platform": "x86_64-centos7-gcc7-opt", "scriptenv": "none", "ncores": 2, "memory": 8589934592, "spark-cluster": "none"}' --delay 30`

   ---
   **warning** <br>
   Before creating servers/sessions make sure you have created users as each server is created for one particular user <br>
   code :
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
        - For single user - `python3 test_check_session.py --port 443 --users user1`
        - For multiple users - `python3 test_check_session.py --port 443 --users user0 user1 user2`

4. **stop_session**

     - Test file : test_stop_session.py
     - Use case : Checks if a session  can be stopped or not
     - To run this test explicitly use -
        - For single user - `python3 test_stop_session.py --port 443 --users user1`
        - For multiple users - `python3 test_stop_session.py --port 443 --users user0 user1 user2`


   
   
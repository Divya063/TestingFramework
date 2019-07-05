#Jupyterhub API tests

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
1. **check_api** corresponds to the test "test_check_api.py" which 
will check hub's sanity by making a GET request to "https://localhost:443/hub/api/".
On successful execution response code should be 200.
    - To run this test explicity use - `python3 test_check_api.py --port 443`
    
2. **create_session** 
   - Test file = test_create_session.py
   - Use case = creates a token and updates the token field in test.yaml file, 
   checks if session can be created successfully or not.
   
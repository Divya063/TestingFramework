1. Creating user's server using jupyterhub api
 - List of the users{"dummy_admin"} is present in adminlist file under srv/jupyterhub, make sure to run the jupyterhub command under srv/jupyterhub
 While, running the jupyterhub command from main directory it was not able to recognize the user "dummy_admin" maybe it is handled by 
 separate config file.
 - Used the command jupyterhub token dummy_admin, and it was recognized by sqlite database.The generated token was added to jupyterhub_config file, 
 as : "c.JupyterHub.service_tokens= {'38dc4701d03848f0819fd958efaf4b4d': 'dummy_admin'}"
 - If you try to add other users other than dummy_admin and you use the command "jupyterhub token dummy_admin" it will not be recognized, using this user with api would give you 403 error, you can create news users using the token generated from username "dummy_admin"
 - Created a user using following command - curl -XPOST -v -k https://localhost:443/hub/api/users -H "Authorization: token 38dc4701d03848f0819fd958efaf4b4d" -d "{ \"usernames\": [ \"enrico\" ], \"admin\": true}" which is quite good.
 - But this user would not be recognized when you try to create a server using the command - curl -XPOST -v -k https://localhost:443/hub/api/users/enrico/server -H “Authorization: token 38dc4701d03848f0819fd958efaf4b4d” - you will get error 500 and errors like -  "KeyError: "getpwnam():" and KeyError: 'platform', (less good)
 - Try to use the those users which are recognized by authentication system that is "user0 - user9". Using these users you will get rid off "KeyError: "getpwnam():" but not KeyError: 'platform'. The KeyError sources from the fact that the spawner for (i.e., the webpage where you select the "Software Stack" and the "Environment Script" to then click "Start my Session") provides to the python spawner some parameters that are passed as environment variables to the user container. If such parameters are not defined, then you get the KeyError.

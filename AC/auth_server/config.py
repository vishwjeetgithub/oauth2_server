# Required for dummy db
# Client secretes
import pandas as pd

## Create dummy db
df_src = [
  {"client_id":12345,"client_secret":"88kjjhhsggdJJH##$"},
  {"client_id":98765,"client_secret":"dfadf0sdf89asdfadsf"},
  {"client_id":23876,"client_secret":"451etwthhzzcvbzfbxh"},
  {"client_id":567483,"client_secret":"cvxvc67567823123123"},
  {"client_id":918273,"client_secret":"plmkmuhuygbtrtf56r5623"}
]

df_client_id_sec = pd.DataFrame(df_src)
# print(df_client_id_sec)


# User login credentials
df_users_src = [
  {"user":1,"password":"1"},
  {"user":2,"password":"2"},
  {"user":3,"password":"3"},
  {"user":4,"password":"4"},
  {"user":5,"password":"5"}
]
df_users = pd.DataFrame(df_users_src)
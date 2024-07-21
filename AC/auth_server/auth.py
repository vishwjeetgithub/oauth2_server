import base64
import cryptography
import json
import jwt
import secrets
import time
import config as config

from cryptography.fernet import Fernet

#KEY = Fernet.generate_key()
KEY = b'YHD1m3rq3K-x6RxT1MtuGzvyLz4EWIJAEkRtBRycDHA='

ISSUER = 'sample-auth-server'
CODE_LIFE_SPAN = 600
JWT_LIFE_SPAN = 1800
ENCRYPT_ALGO = 'RS256' #Cannot change. Keys are public and private and should be changed to change the Algo 


authorization_codes = {}

f = Fernet(KEY)

with open('private.pem', 'rb') as file:
  private_key = file.read()

def authenticate_user_credentials(username, password):
  df_users = config.df_users
  df_user_row = df_users[df_users['user']==int(username)]
  # Debug
  # print("user iloc :: ",df_user_row.iloc[0,0],"password iloc :: ",df_user_row.iloc[0,1])
  if (df_user_row.iloc[0,0] == int(username) and df_user_row.iloc[0,1] == password):
    return True
  else:
    return False

def authenticate_client(client_id, client_secret):
  return True

def verify_client_info(client_id, redirect_url):
  # Debug
  # print("entered client info verification")
  # global temp_int_var
  # temp_int_var +=1
  # print("Temp in var :::::::::::::: ", temp_int_var)
  df_client_id_sec = config.df_client_id_sec
  df_client_id_sec_row = df_client_id_sec[df_client_id_sec['client_id']==int(client_id)]
  # Debug
  #  and df_client_id_sec_row.iloc[0,0] == int(client_id)
  if (len(df_client_id_sec_row.index)>0):
    # print("cliend_id iloc :: ",df_client_id_sec_row.iloc[0,0],"client_secret iloc :: ",df_client_id_sec_row.iloc[0,1], " :: ",len(df_client_id_sec_row.index))
    return True
  else:
    # Debug
    # print("client id not found")
    return False

def generate_access_token():
  payload = {
    "iss": ISSUER,
    "exp": time.time() + JWT_LIFE_SPAN
  }

  access_token = jwt.encode(payload, private_key, algorithm = ENCRYPT_ALGO)

  return access_token

def generate_authorization_code(client_id, redirect_url):
  #f = Fernet(KEY)
  authorization_code = f.encrypt(json.dumps({
    "client_id": client_id,
    "redirect_url": redirect_url,
  }).encode())

  authorization_code = base64.b64encode(authorization_code, b'-_').decode().replace('=', '')

  expiration_date = time.time() + CODE_LIFE_SPAN
  
  global authorization_codes
  
  authorization_codes[authorization_code] = {
    "client_id": client_id,
    "redirect_url": redirect_url,
    "exp": expiration_date
  }
  # Debug
  # print("Authorization codes :: ", authorization_codes," :: length of auth codes dict :: ", len(authorization_codes))
  return authorization_code

def verify_authorization_code(authorization_code, client_id, redirect_url):
  #f = Fernet(KEY)
  record = authorization_codes.get(authorization_code)
  if not record:
    return False

  client_id_in_record = record.get('client_id')
  redirect_url_in_record = record.get('redirect_url')
  exp = record.get('exp')

  if client_id != client_id_in_record or \
     redirect_url != redirect_url_in_record:
    return False

  if exp < time.time():
    return False

  del authorization_codes[authorization_code]

  return True

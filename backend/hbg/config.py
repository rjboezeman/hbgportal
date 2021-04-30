import os, sys
from pydantic import BaseSettings

class Settings(BaseSettings):
  app_name: str = "Heartbeat Games API"
  admin_email: str = "info@heartbeat.games"

  authjwt_secret_key: str = "secret"
  authjwt_token_location: set = {"cookies"}  # Configure application to store and get JWT from cookies
  authjwt_cookie_csrf_protect: bool = True # Enable/disable CSRF Protection. default is True
  authjwt_cookie_samesite: str = 'none' # Change to 'lax' in production to make your website more secure from CSRF Attacks, default is None
  authjwt_cookie_secure: bool = False # If the secure flag is True cookie can only be transmitted securely over HTTPS. For production set to True
  authjwt_access_token_expires: int = 30  # in minutes

  ACCESS_TOKEN_EXPIRE_MINUTES: int = 1
  ALGORITHM: str = "HS256"
  MAX_LOGIN_ATTEMPTS: int = 5 
  SECRET_KEY: str = "not so secret yet"
  mandatory_envs: list = [
                "MONGODBSRV",
                "MONGODB",
                "SECRET_KEY"
              ]

  safeOrigins = [
      "http://localhost:8080",
      "http://172.17.156.38:8080",
      "https://portal.dev.heartbeat.games",
      "https://portal.acc.heartbeat.games",
      "https://portal.heartbeat.games",
  ]



  def checkEnvs(self):
    for manenv in self.mandatory_envs:
      if manenv not in os.environ:
        print(f"Mandatory environment variable missing, exiting now: {manenv}")
        sys.exit()
  
  class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


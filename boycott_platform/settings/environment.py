import os
from environs import Env

env = Env()
env_file = os.getenv("ENV_FILE", ".env")
if env_file:
    env.read_env(env_file)
else:
    raise FileNotFoundError("No environment file found (.env)")
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv() 

conn = psycopg2.connect(os.environ["DB_STRING"])
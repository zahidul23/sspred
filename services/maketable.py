import os
import json
from services import batchtools
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import sql


conn = batchtools.getConn()
cursor = conn.cursor()

create_table_query = '''CREATE TABLE IF NOT EXISTS seqtable
          (ID TEXT PRIMARY KEY     NOT NULL,
          SEQ TEXT NOT NULL,
          PSIPRED TEXT,
          PSICONF TEXT,
          PSISTAT INT,
          PSIMSG TEXT,

          PSSPRED TEXT,
          PSSCONF TEXT,
          PSSSTAT INT,
          PSSMSG TEXT,

          JPREDPRED TEXT,
          JPREDCONF TEXT,
          JPREDSTAT INT,
          JPREDMSG TEXT,

          RAPTORXPRED TEXT,
          RAPTORXCONF TEXT,
          RAPTORXSTAT INT,
          RAPTORXMSG TEXT,

          YASPINPRED TEXT,
          YASPINCONF TEXT,
          YASPINSTAT INT,
          YASPINMSG TEXT,

          SABLEPRED TEXT,
          SABLECONF TEXT,
          SABLESTAT INT,
          SABLEMSG TEXT,

          SSPROPRED TEXT,
          SSPROCONF TEXT,
          SSPROSTAT INT,
          SSPROMSG TEXT,
        
      MAJORITYVOTE TEXT,
      PDB TEXT,
      PDBID TEXT
); '''

add_timestamp_column  = '''
ALTER TABLE seqtable
ADD COLUMN IF NOT EXISTS timestamp_creation timestamptz,
ADD COLUMN IF NOT EXISTS timestamp_update timestamptz;
'''

cursor.execute(create_table_query)
cursor.execute(add_timestamp_column)
conn.commit()
cursor.close()

if conn:
	conn.close()
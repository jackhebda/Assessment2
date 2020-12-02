from sqlalchemy import *
import csv

engine = create_engine('postgres://jack:jack@localhost/exam', echo = False)
conn = engine.connect()

with open('/home/jack/Documents/python/exam/app/data/zipcodes.csv', newline='') as f:
        zipcode_dict = {}
        reader = csv.reader(f)
        for row in reader:
            if len(row[0]) == 4:
                zipcode_dict[int(row[0])] = row[1]
            else:
                for zip in range(int(row[0][:4]), int(row[0][7:]) + 1):
                    zipcode_dict[zip] = row[1]

metadata = MetaData()

riskfactor = Table('riskfactor', metadata,
    Column('zipcode', Integer, primary_key=True),
    Column('risk_factor', String))                
                  
metadata.create_all(engine)

for k, v in zipcode_dict.items():
    conn.execute(insert(riskfactor).values(zipcode = k, risk_factor = v))

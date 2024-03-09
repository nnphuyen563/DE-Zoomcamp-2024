import pandas as pd
from sqlalchemy import create_engine
from time import time
import argparse
import os

def main(params):
    user = params.user
    password = params.password
    host = params.host 
    port = params.port 
    db = params.db
    table_name = params.table_name
    url = params.url
    
    # the backup files are gzipped, and it's important to keep the correct extension
    # for pandas to be able to open the file
    if url.endswith('.csv.gz'):
        csv_name = 'output.csv.gz'
    else:
        csv_name = 'output.csv'

    os.system(f"wget {url} -O {csv_name}")

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)

    df = next(df_iter)

    df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
    df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

    df.to_sql(name=table_name, con=engine, if_exists='append')


    while True: 

        try:
            t_start = time()
            
            df = next(df_iter)

            df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
            df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

            df.to_sql(name=table_name, con=engine, if_exists='append')

            t_end = time()

            print('inserted another chunk, took %.3f second' % (t_end - t_start))

        except StopIteration:
            print("Finished ingesting data into the postgres database")
            break
        # for chunk in pd.read_csv('yellow_tripdata_2021-01.csv', chunksize=10000):  # Adjust chunksize as needed
        #     t_start = time()

        #     chunk.tpep_pickup_datetime = pd.to_datetime(chunk.tpep_pickup_datetime)
        #     chunk.tpep_dropoff_datetime = pd.to_datetime(chunk.tpep_dropoff_datetime)

        #     chunk.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')

        #     t_end = time()

        #     print('Inserted another chunk, took %.3f seconds' % (t_end - t_start))


if __name__ == '__main__':

        parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

        parser.add_argument('--user', help='user name for postgres')
        parser.add_argument('--password', help='password for postgres')
        parser.add_argument('--host', help='host for postgres')
        parser.add_argument('--port', help='port for postgres')
        parser.add_argument('--db', help='database name for postgres')
        parser.add_argument('--table_name', help='name of the table where we will write the results to')
        parser.add_argument('--url', help='url of the CSV file')

        args = parser.parse_args()
        
        main(args)




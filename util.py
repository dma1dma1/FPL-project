import psycopg2
from config import config

def connect(command):
    try:
        # Get connection params
        params = config()

        # Connect to PostgreSQL
        print('Connecting to PostgreSQL database...')
        conn = psycopg2.connect(**params)
        print('Connected!')

        # Create cursor
        cur = conn.cursor()

        # Executing command
        print('Executing command...')
        cur.execute(open(command, 'r').read())
        print('Finished executing!')

        # Close connection
        cur.close()

        # Commit changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn:
            cur.close()
            conn.close()
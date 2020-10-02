import psycopg2

def createTables():
    conn = None
    try:
        conn = psycopg2.connect()
        cur = conn.cursor()
        cur.close()
        cur.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

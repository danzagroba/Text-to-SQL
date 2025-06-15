import mysql.connector
import psycopg2
from psycopg2 import Error

DB_CONFIG_MS = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'Orders'
}

DB_CONFIG_PG = {
    'host': 'localhost',
    'database': 'postgres',
    'user': 'postgres',
    'password': '',
    'port': '5432'
}


def executar_query_e_obter_results_mysql(query_sql, data=None):
    conn = None
    cursor = None
    results = None

    try:
        conn = mysql.connector.connect(**DB_CONFIG_MS)
        print("Conexão MySQL estabelecida com sucesso!")

        cursor = conn.cursor()

        cursor.execute(query_sql, data)

        if query_sql.strip().upper().startswith("SELECT"):
            results = cursor.fetchall()
            print(f"Query '{query_sql.strip()}' executada. {len(results)} linhas retornadas.")
        else:
            conn.commit()
            results = cursor.rowcount
            print(f"Query '{query_sql.strip()}' executada. {results} linhas afetadas.")

    except Error as err:
        print(f"Erro ao executar a query MySQL: {err}")
        if conn:
            conn.rollback()
        results = None 

    finally:
        if cursor:
            cursor.close()
            print("Cursor MySQL fechado.")
        if conn:
            conn.close()
            print("Conexão MySQL fechada.")
    
    return results

def executar_query_e_obter_results_postgresql(query_sql, data=None):
    conn = None
    cursor = None
    results = None

    try:
        conn = psycopg2.connect(**DB_CONFIG_PG)
        print("Conexão estabelecida com sucesso!")

        cursor = conn.cursor()
        cursor.execute(query_sql, data)

        if query_sql.strip().upper().startswith("SELECT"):
            results = cursor.fetchall()
            print(f"Query '{query_sql}' executada. {len(results)} linhas retornadas.")
        else:
            conn.commit()
            results = cursor.rowcount
            print(f"Query '{query_sql}' executada. {results} linhas afetadas.")

    except Error as err:
        print(f"Erro ao executar a query: {err}")
        if conn:
            conn.rollback()
        results = None 

    finally:
        if cursor:
            cursor.close()
            print("Cursor fechado.")
        if conn:
            conn.close()
            print("Conexão fechada.")
    
    return results

if __name__ == "__main__":
    #MySQL

    select_query = """
    select * from Customers
    """
    datamysql = executar_query_e_obter_results_mysql(select_query)
    print(datamysql)

    #PostgreSQL
    
    select_query_pg = """
    select * from Customers
    """
    datapostgresql = executar_query_e_obter_results_postgresql(select_query_pg)
    print(datapostgresql)
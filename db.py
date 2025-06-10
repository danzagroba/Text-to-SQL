import mysql.connector
import psycopg2
from psycopg2 import Error

DB_CONFIG_MS = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'University'
}

DB_CONFIG_PG = {
    'host': 'localhost',
    'database': 'postgres',
    'user': 'postgres',
    'password': '',
    'port': '5432'
}


def executar_query_e_obter_resultados_mysql(query_sql, dados=None):
    conn = None
    cursor = None
    resultados = None

    try:
        conn = mysql.connector.connect(**DB_CONFIG_MS)
        print("Conexão MySQL estabelecida com sucesso!")

        cursor = conn.cursor()

        cursor.execute(query_sql, dados)

        if query_sql.strip().upper().startswith("SELECT"):
            resultados = cursor.fetchall()
            print(f"Query '{query_sql.strip()}' executada. {len(resultados)} linhas retornadas.")
        else:
            conn.commit()
            resultados = cursor.rowcount
            print(f"Query '{query_sql.strip()}' executada. {resultados} linhas afetadas.")

    except Error as err:
        print(f"Erro ao executar a query MySQL: {err}")
        if conn:
            conn.rollback()
        resultados = None 

    finally:
        if cursor:
            cursor.close()
            print("Cursor MySQL fechado.")
        if conn:
            conn.close()
            print("Conexão MySQL fechada.")
    
    return resultados

def executar_query_e_obter_resultados_postgresql(query_sql, dados=None):
    conn = None
    cursor = None
    resultados = None

    try:
        conn = psycopg2.connect(**DB_CONFIG_PG)
        print("Conexão estabelecida com sucesso!")

        cursor = conn.cursor()
        cursor.execute(query_sql, dados)

        if query_sql.strip().upper().startswith("SELECT"):
            resultados = cursor.fetchall()
            print(f"Query '{query_sql}' executada. {len(resultados)} linhas retornadas.")
        else:
            conn.commit()
            resultados = cursor.rowcount
            print(f"Query '{query_sql}' executada. {resultados} linhas afetadas.")

    except Error as err:
        print(f"Erro ao executar a query: {err}")
        if conn:
            conn.rollback()
        resultados = None 

    finally:
        if cursor:
            cursor.close()
            print("Cursor fechado.")
        if conn:
            conn.close()
            print("Conexão fechada.")
    
    return resultados

if __name__ == "__main__":
    #MySQL

    criar_tabela_query = """
    select * from student
    """
    dadosmysql = executar_query_e_obter_resultados_mysql(criar_tabela_query)
    print(dadosmysql)

    #PostgreSQL
    
    criar_tabela_query_pg = """
    select * from student
    """
    dadospostgresql = executar_query_e_obter_resultados_postgresql(criar_tabela_query_pg)
    print(dadospostgresql)
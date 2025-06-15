#Interface
import tkinter as tk
from tkinter import Radiobutton, IntVar, W, Label, Entry, Frame, Text

#DBs
import mysql.connector
import psycopg2
from psycopg2 import Error

#AI model
from transformers import AutoTokenizer, AutoModelForCausalLM
import os

os.environ["TRANSFORMERS_OFFLINE"] = "1"
model_path = "/home/hmm/.cache/huggingface/hub/models--NumbersStation--nsql-350M/snapshots/6146518e469bbfcee8d3551edd432a312f1fe777"

tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
model = AutoModelForCausalLM.from_pretrained(model_path, local_files_only=True)


#MySQL and PostgreSQL connection configuration
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

def create_query(message: str, val: int, output_widget):
    output_widget.config(state="normal")
    output_widget.delete("1.0", "end")
    if (message == ""):
        output_widget.insert("1.0", "Insira um texto")
        return

    if (val == 0):
        output_widget.insert("1.0", "Escolha um banco de dados")
        return
    
    text = """CREATE TABLE Customers (
CustomerID INT PRIMARY KEY AUTO_INCREMENT,
Name VARCHAR(50),
Email VARCHAR(30)
);

CREATE TABLE Orders (
    OrderID INT PRIMARY KEY AUTO_INCREMENT,
    CustomerID INT,
    OrderDate DATE,
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);

CREATE TABLE Products (
    ProductID INT PRIMARY KEY AUTO_INCREMENT,
    ProductName VARCHAR(100),
    Price DECIMAL(10,2)
);

CREATE TABLE OrderDetails (
    DetailID INT PRIMARY KEY AUTO_INCREMENT,
    OrderID INT,
    ProductID INT,
    Quantity INT,
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);

"""

    if (val == 1):
        text = text + "\n-- Using valid MySQL, answer the following questions for the tables provided above."
    elif (val == 2):
        text = text + "\n-- Using valid PostgreSQL, answer the following questions for the tables provided above."
    text = text + "\n -- " +  message
    inputs = tokenizer(text, return_tensors="pt")
    generated_ids = model.generate(
        input_ids=inputs.input_ids,
        attention_mask=inputs.attention_mask,
        max_length=1000
    )
    full_output = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
    print(full_output)
    query = "SELECT "+full_output.split("SELECT")[-1].strip()
    output_widget.insert("1.0", query)
    output_widget.config(state="disabled")
    
def run_query(query: str, val: int):
    if (query == ""):
        return
    
    if(val == 1):
        table = running_ms_query(query)
    else:
        table = running_ps_query(query)

    print(table)


#MySQL and PostgreSQL functions
def running_ms_query(query_sql, data=None):
    conn = None
    cursor = None
    results = None

    try:
        conn = mysql.connector.connect(**DB_CONFIG_MS)
        print("Connection with MySQL sucessful!")

        cursor = conn.cursor()

        cursor.execute(query_sql, data)

        if query_sql.strip().upper().startswith("SELECT"):
            results = cursor.fetchall()
            print(f"Query '{query_sql.strip()}' executed. {len(results)} returned rows.")
        else:
            conn.commit()
            results = cursor.rowcount
            print(f"Query '{query_sql.strip()}' executed. {len(results)} returned rows.")

    except Error as err:
        print(f"Error running MySQL query: {err}")
        if conn:
            conn.rollback()
        results = err

    finally:
        if cursor:
            cursor.close()
            print("Cursor MySQL closed.")
        if conn:
            conn.close()
            print("Conection MySQL closed.")
    
    return results

def running_ps_query(query_sql, data=None):
    conn = None
    cursor = None
    results = None

    try:
        conn = psycopg2.connect(**DB_CONFIG_PG)
        print("Connection with PostgreSQL sucessful!")

        cursor = conn.cursor()
        cursor.execute(query_sql, data)

        if query_sql.strip().upper().startswith("SELECT"):
            results = cursor.fetchall()
            print(f"Query '{query_sql.strip()}' executed. {len(results)} returned rows.")
        else:
            conn.commit()
            results = cursor.rowcount
            print(f"Query '{query_sql.strip()}' executed. {len(results)} returned rows.")

    except Error as err:
        print(f"Error running PostgreSQL query: {err}")
        if conn:
            conn.rollback()
        results = None 

    finally:
        if cursor:
            cursor.close()
            print("Cursor PostgreSQL closed.")
        if conn:
            conn.close()
            print("Conection PostgreSQL closed.")
    
    return results



root = tk.Tk(screenName = None, baseName=None, className='Text-to-SQL', useTk=1)


w = Label(root, text='Selecione o banco de data:')
w.pack()

frame_db = Frame(root)
frame_db.pack()
v = IntVar()
Radiobutton(frame_db, text='MySQL', variable=v, value=1).pack(side=tk.LEFT, padx=5)
Radiobutton(frame_db, text='PostgreSQL', variable=v, value=2).pack(side=tk.LEFT, padx=5) 

w = Label(root, text='Text-to-SQL:')
w.pack()

e1 = Text(root, height=5, width=40)
e1.pack()

b1 = tk.Button(root, text='Gerar Query', width=25, command= lambda: create_query(e1.get("1.0", "end").strip(), v.get(), e2))
b1.pack()

w = Label(root, text='Resultado:')
w.pack()

e2 = Text(root, height=5, width=40)
e2.pack()
e2.config(state="disabled")

b2 = tk.Button(root, text='Rodar Query', width=25, command= lambda: run_query(e2.get("1.0", "end"), v.get()))
b2.pack()

root.mainloop()
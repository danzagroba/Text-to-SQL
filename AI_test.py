from transformers import AutoTokenizer, AutoModelForCausalLM
import os

os.environ["TRANSFORMERS_OFFLINE"] = "1"
model_path = "/home/hmm/.cache/huggingface/hub/models--NumbersStation--nsql-350M/snapshots/6146518e469bbfcee8d3551edd432a312f1fe777"

tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
model = AutoModelForCausalLM.from_pretrained(model_path, local_files_only=True)



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

-- Using valid SQLite, answer the following questions for the tables provided above.

--Do a table with all the products and the orders besides it

SELECT"""

inputs = tokenizer(text, return_tensors="pt")

generated_ids = model.generate(
    input_ids=inputs.input_ids,
    attention_mask=inputs.attention_mask,
    max_length=1000
)
print(tokenizer.decode(generated_ids[0], skip_special_tokens=True))
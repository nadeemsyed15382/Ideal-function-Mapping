# Ideal Function Mapping (IU DLMDSPWP01 – Programming with Python)

![Python](https://img.shields.io/badge/Python-3.13-blue.svg)
![Pandas](https://img.shields.io/badge/Pandas-DataFrame-lightgrey.svg)
![NumPy](https://img.shields.io/badge/NumPy-Math%20Library-orange.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-SQLite-green.svg)
![Bokeh](https://img.shields.io/badge/Bokeh-Interactive%20Plots-purple.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## Overview
This project is an implementation of the **Ideal Function Mapping** assignment for the IU course  
**DLMDSPWP01 – Programming with Python**.  

It demonstrates a complete Python pipeline for:
- Loading and validating CSV datasets
- Selecting the **best-fit ideal functions** based on the **least-squares deviation rule**
- Mapping test data points to the selected ideal functions using the **√2 deviation criterion**
- Storing all results in a **SQLite database**
- Creating an **interactive Bokeh visualization**

---

##  Features
- **Object-Oriented Design (OOP)** with inheritance and custom exceptions  
- **Automated database creation** using SQLAlchemy  
- **Efficient vectorized calculations** via NumPy  
- **Interactive visual output** rendered in HTML  
- **Unit tests** for core components 
---
##  Project Structure
python_function_mapping/
│
├── data/
│ ├── train.csv
│ ├── ideal.csv
│ └── test.csv
│
├── src/
│ ├── data_loader.py
│ ├── database_manager.py
│ ├── function_selector.py
│ ├── mapper.py
│ ├── visualizer.py
│ ├── exceptions.py
│ └── main.py
│
├── tests/
│ └── test_suite.py
│
├── requirements.txt
└── README.md


---

## Installation
Clone the repository and create a virtual environment:

```bash
git clone https://github.com/nadeemsyed15382/Ideal-function-Mapping.git
cd Ideal-function-Mapping

python -m venv venv
# activate environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
Run the Program
python -m src.main


##  Methodology

Least-Squares Selection
Each training function 
𝑦
𝑡
𝑟
𝑎
𝑖
𝑛
y
train
	​

 is compared with all 50 ideal functions.
The function minimizing the total squared error is selected.

LSD
𝑗
=
∑
(
𝑦
𝑡
𝑟
𝑎
𝑖
𝑛
−
𝑦
𝑖
𝑑
𝑒
𝑎
𝑙
𝑗
)
2
LSD
j
	​

=∑(y
train
	​

−y
ideal
j
	​

	​

)
2

√2 Mapping Rule
Test points are mapped only if their deviation ≤ √2 × (max training deviation).

Visualization
All training, ideal, and mapped test data are plotted using Bokeh.

🧾 Database Tables
Table	Description
training_data	Original training datasets (x, y1–y4)
ideal_functions	50 ideal functions (x, y1–y50)
test_data_raw	Original test data (x, y)
mapped_test_data	Mapped results with deviation
📊 Example Output

function_mapping_visual.html

Interactive plot showing:

Solid lines → Training functions

Dashed lines → Ideal functions

Red dots → Test points successfully mapped

🧩 Technologies Used

Python 3.13

NumPy, Pandas

SQLAlchemy (SQLite)

Bokeh (interactive visualization)

Pytest (unit testing)

## Author
Developed by Syed Nadeem

as part of IU International University’s Data Science module: Programming with Python (DLMDSPWP01).

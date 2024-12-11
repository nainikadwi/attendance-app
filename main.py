from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import csv
import os
from datetime import datetime, timedelta

app = FastAPI()

# Constants
ADMIN_PASSWORD = "admin123"
BASE_DIR = "attendance_records"
CURRENT_MONTH_FILE = f"{BASE_DIR}/attendance_{datetime.now().strftime('%Y_%m')}.csv"

# Ensure the attendance directory exists
os.makedirs(BASE_DIR, exist_ok=True)

# Helper Functions
def initialize_csv():
    """Ensure a CSV file exists for the current month."""
    if not os.path.exists(CURRENT_MONTH_FILE):
        with open(CURRENT_MONTH_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            # Write the header with dates for the current month
            start_date = datetime.now().replace(day=1)
            end_date = (start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            dates = [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range((end_date - start_date).days + 1)]
            writer.writerow(["Employee Name"] + dates)

def get_csv_data():
    """Read data from the CSV."""
    initialize_csv()
    with open(CURRENT_MONTH_FILE, mode="r") as file:
        reader = csv.reader(file)
        rows = list(reader)
    return rows

def write_csv_data(rows):
    """Write data to the CSV."""
    with open(CURRENT_MONTH_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)

@app.get("/", response_class=HTMLResponse)
async def home():
    """Display the attendance page with improved styling."""
    rows = get_csv_data()
    headers = rows[0]
    today = datetime.now().strftime('%Y-%m-%d')

    # Generate HTML table for displaying attendance and checkboxes
    table_html = """
    <table>
        <thead>
            <tr>""" + "".join(f"<th>{header}</th>" for header in headers) + "</tr>" + """
        </thead>
        <tbody>
    """
    for row in rows[1:]:
        table_html += "<tr>"
        for i, cell in enumerate(row):
            if i == 0:  # Employee Name
                table_html += f"<td>{cell}</td>"
            elif headers[i] == today:  # Current Date
                # Pre-check the checkbox if the cell value is "Present"
                is_checked = "checked" if cell == "Present" else ""
                table_html += f"<td><input type='checkbox' name='attendance' value='{row[0]}' {is_checked}></td>"
            else:  # Past/Future Dates
                table_html += f"<td>{cell}</td>"
        table_html += "</tr>"
    table_html += "</tbody></table>"

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f9f9f9;
                color: #333;
            }}
            h1 {{
                text-align: center;
                margin: 20px 0;
                color: #4CAF50;
            }}
            .container {{
                max-width: 800px;
                margin: 20px auto;
                padding: 20px;
                background-color: #fff;
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 20px;
            }}
            table th, table td {{
                border: 1px solid #ddd;
                padding: 10px;
                text-align: center;
            }}
            table th {{
                background-color: #f2f2f2;
                font-weight: bold;
            }}
            table tbody tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}
            form {{
                margin-bottom: 20px;
            }}
            form input[type="text"],
            form input[type="password"] {{
                width: calc(100% - 20px);
                padding: 8px;
                margin: 10px 0;
                border: 1px solid #ccc;
                border-radius: 4px;
            }}
            button {{
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                margin-top: 10px;
                cursor: pointer;
                border-radius: 4px;
                font-size: 14px;
            }}
            button:hover {{
                background-color: #45a049;
            }}
            .form-container {{
                display: flex;
                flex-direction: column;
                gap: 20px;
            }}
        </style>
    </head>
    <body>
<div class="container">
            <h1>Attendance Management</h1>
            
            <!-- Admin Actions for Adding and Deleting Employees -->
            <div class="form-container">
                <form method="post" action="/add_employee">
                    <label for="add-employee">Add Employee:</label>
                    <input type="text" id="add-employee" name="employee_name" placeholder="Employee Name" required>
                    <input type="password" name="admin_password" placeholder="Admin Password" required>
                    <button type="submit">Add Employee</button>
                </form>

                <form method="post" action="/delete_employee">
                    <label for="delete-employee">Delete Employee:</label>
                    <input type="text" id="delete-employee" name="employee_name" placeholder="Employee Name" required>
                    <input type="password" name="admin_password" placeholder="Admin Password" required>
                    <button type="submit">Delete Employee</button>
                </form>
            </div>

            <!-- Attendance Table -->
            <form method="post" action="/submit_attendance">
                {table_html}
                <button type="submit">Submit Attendance</button>
            </form>
        </div>
    </body>
    </html>
    """

@app.post("/submit_attendance")
async def submit_attendance(attendance: list[str] = Form(...)):
    """Mark attendance for the current date."""
    today = datetime.now().strftime('%Y-%m-%d')
    rows = get_csv_data()
    headers = rows[0]
    
    # Mark attendance as "Present" for those checked
    for row in rows[1:]:
        if row[0] in attendance:
            row[headers.index(today)] = "Present"
    
    write_csv_data(rows)
    return {"message": "Attendance submitted successfully!"}

@app.post("/add_employee")
async def add_employee(employee_name: str = Form(...), admin_password: str = Form(...)):
    """Add a new employee (Admin Only)."""
    if admin_password != ADMIN_PASSWORD:
        return {"message": "Invalid admin password!"}
    
    rows = get_csv_data()
    if any(row[0] == employee_name for row in rows[1:]):
        return {"message": "Employee already exists!"}
    
    # Add the new employee with no attendance data for the month
    rows.append([employee_name] + [""] * (len(rows[0]) - 1))
    write_csv_data(rows)
    
    return {"message": f"Employee '{employee_name}' added successfully!"}

@app.post("/delete_employee")
async def delete_employee(employee_name: str = Form(...), admin_password: str = Form(...)):
    """Delete an employee (Admin Only)."""
    if admin_password != ADMIN_PASSWORD:
        return {"message": "Invalid admin password!"}
    
    rows = get_csv_data()
    rows = [row for row in rows if row[0] != employee_name]
    write_csv_data(rows)
    
    return {"message": f"Employee '{employee_name}' deleted successfully!"}

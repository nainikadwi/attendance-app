import logging
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import csv
import os
from datetime import datetime, timedelta

app = FastAPI()

# Constants
ADMIN_PASSWORD = "admin123"
BASE_DIR = "attendance_records"
LOG_DIR = "logs"
CURRENT_MONTH_FILE = f"{BASE_DIR}/attendance_{datetime.now().strftime('%Y_%m')}.csv"

# Ensure directories exist
os.makedirs(BASE_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# Configure Logging
logging.basicConfig(
    filename=f"{LOG_DIR}/attendance.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Helper Functions
def initialize_csv():
    """Ensure a CSV file exists for the current month."""
    if not os.path.exists(CURRENT_MONTH_FILE):
        logging.info("Initializing new CSV for the current month.")
        with open(CURRENT_MONTH_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
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
    logging.info("Fetched data from the CSV.")
    return rows

def write_csv_data(rows):
    """Write data to the CSV."""
    with open(CURRENT_MONTH_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)
    logging.info("Updated data written to the CSV.")

@app.get("/", response_class=HTMLResponse)
async def home():
    """Display the attendance page."""
    logging.info("Rendering attendance management page.")
    rows = get_csv_data()
    headers = rows[0]
    today = datetime.now().strftime('%Y-%m-%d')

    # Generate HTML table for displaying attendance and checkboxes
    table_html = "<table border='1'><tr>" + "".join(f"<th>{header}</th>" for header in headers) + "</tr>"
    
    for row in rows[1:]:
        table_html += "<tr>"
        for i, cell in enumerate(row):
            if i == 0:  # Employee Name
                table_html += f"<td>{cell}</td>"
            elif headers[i] == today:  # Current Date
                checked = "checked" if cell == "1" else ""
                table_html += f"<td><input type='checkbox' name='attendance' value='{row[0]}' {checked}></td>"
            else:  # Past/Future Dates
                table_html += f"<td>{cell}</td>"
        table_html += "</tr>"
    table_html += "</table>"

    return f"""
<!DOCTYPE html>
    <html>
    <head>
        <style>
            .form-container {{
                display: flex;
                justify-content: space-between;
                margin-bottom: 20px;
                width: 100%;
            }}
            .form-container input {{
                margin-right: 10px;
                width: 200px;
            }}
            .button-container {{
                display: flex;
                justify-content: space-between;
                width: 100%;
            }}
            .button-container button {{
                margin-right: 10px;
            }}
        </style>
    </head>
    <body>
        <h1>Attendance Management</h1>
        
        <form method="post" action="/add_employee">
            <input type="text" name="employee_name" placeholder="Employee Name" required>
            <input type="password" name="admin_password" placeholder="Admin Password" required>
            <button type="submit">Add Employee</button>
        </form>

        <form method="post" action="/delete_employee">
            <input type="text" name="employee_name" placeholder="Employee Name" required>
            <input type="password" name="admin_password" placeholder="Admin Password" required>
            <button type="submit">Delete Employee</button>
        </form>

        <form method="post" action="/submit_attendance">
            {table_html}
            <button type="submit">Submit Attendance</button>
        </form>
    </body>
    </html>
    """

@app.post("/submit_attendance")
async def submit_attendance(attendance: list[str] = Form(...)):
    """Mark attendance for the current date."""
    today = datetime.now().strftime('%Y-%m-%d')
    rows = get_csv_data()
    headers = rows[0]
    
    # Update attendance
    for row in rows[1:]:
        if row[0] in attendance:
            row[headers.index(today)] = "1"
        elif headers.index(today) < len(row):
            row[headers.index(today)] = "0"
    
    write_csv_data(rows)
    logging.info(f"Attendance submitted for {len(attendance)} employees.")
    return {"message": "Attendance submitted successfully!"}

@app.post("/add_employee")
async def add_employee(employee_name: str = Form(...), admin_password: str = Form(...)):
    """Add a new employee (Admin Only)."""
    if admin_password != ADMIN_PASSWORD:
        logging.warning("Failed add employee attempt: Invalid admin password.")
        return {"message": "Invalid admin password!"}
    
    rows = get_csv_data()
    if any(row[0] == employee_name for row in rows[1:]):
        logging.warning(f"Attempt to add duplicate employee: {employee_name}.")
        return {"message": "Employee already exists!"}
    
    rows.append([employee_name] + ["0"] * (len(rows[0]) - 1))
    write_csv_data(rows)
    logging.info(f"Employee '{employee_name}' added successfully.")
    return {"message": f"Employee '{employee_name}' added successfully!"}

@app.post("/delete_employee")
async def delete_employee(employee_name: str = Form(...), admin_password: str = Form(...)):
    """Delete an employee (Admin Only)."""
    if admin_password != ADMIN_PASSWORD:
        logging.warning("Failed delete employee attempt: Invalid admin password.")
        return {"message": "Invalid admin password!"}
    
    rows = get_csv_data()
    if not any(row[0] == employee_name for row in rows[1:]):
        logging.warning(f"Attempt to delete non-existent employee: {employee_name}.")
        return {"message": "Employee not found!"}

    rows = [row for row in rows if row[0] != employee_name]
    write_csv_data(rows)
    logging.info(f"Employee '{employee_name}' deleted successfully.")
    return {"message": f"Employee '{employee_name}' deleted successfully!"}

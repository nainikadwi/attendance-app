The Real-Time Attendance Management System is a web-based application built using FastAPI that allows employees to log their attendance in real-time by marking themselves as Present or Absent. The system captures the attendance along with the exact timestamp and stores the records in a CSV file for easy tracking and future reference.

# Features:

1.	User-Friendly Interface:
•	Employees can input their Employee ID, Name, and select their attendance status (Present or Absent).
2.	Real-Time Logging:
•	Attendance records are logged instantly with an accurate timestamp of when the entry was made.
3.	Data Storage:
•	Attendance is saved in a CSV file, with the following columns: Timestamp, Employee ID, Name, and Status.
4.	Timezone Handling:
•	The system records timestamps based on the local timezone, ensuring accurate attendance logging across regions.
5.	Error Handling:
•	Errors during attendance logging (e.g., file writing issues or invalid inputs) are handled and logged for troubleshooting.

# Technology Stack:

•	FastAPI: For building the API.
•	CSV: For storing attendance data.
•	Pytz: For managing timezone-aware timestamps.
•	Logging: For error tracking.

# How It Works:

1.	Employees input their Employee ID, Name, and attendance status (Present/Absent).
2.	Upon submission, the system logs the data (timestamp, employee details, and status) into a CSV file.
3.	The CSV file is updated in real-time with the attendance data.
4.	Any errors encountered during the process are logged for easier debugging.
   
Example CSV Record:
Timestamp, Employee_ID, Name, Status

# Benefits:

•	Real-Time Updates: Attendance is logged immediately.
•	Accurate Timestamps: Ensures precise record-keeping.
•	Simple & Lightweight: Easy to implement and use, ideal for small to medium-sized organizations.
•	Error Logging: Captures errors for smooth operation.

# Conclusion:

The Real-Time Attendance Management System efficiently manages employee attendance with real-time updates and accurate timestamp logging. It provides an easy-to-use solution for tracking attendance and ensures smooth operations with error handling and logging.# attendance-app

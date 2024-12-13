import frappe
from datetime import datetime


def execute(filters=None):
    # Prepare the query criteria
    filters_criteria = {"date_of_birth": ["is", "set"]}

    birthday_month = filters.get("birthday_month")
    employment_status = filters.get("employment_status")

    if employment_status == "Active":
        filters_criteria["employment_status"] = "Active"
    elif employment_status == "Inactive":
        filters_criteria["employment_status"] = ["!=", "Active"]

    # Get employee data
    employees = frappe.get_all("Employee", filters=filters_criteria, fields=["employee_name", "date_of_birth", "age", "employment_status", "tenure", "employee_code", "name"])
    
    report_data = sorted(
        [
            {
                "employee_name": f'<a href="/app/employee/{emp.employee_code}">{emp.employee_name}</a>',
                "formatted_date_of_birth": emp.date_of_birth.strftime("%d %B") if emp.date_of_birth else "N/A",
                "age": str(emp.age) if emp.age is not None else "N/A",
                "employment_status": emp.employment_status,
                "tenure": emp.tenure,
                "employee_code": emp.employee_code
            }
            for emp in employees
            if not birthday_month or (emp.date_of_birth and emp.date_of_birth.month == datetime.strptime(birthday_month, "%B").month)
        ],
        key=lambda x: x['formatted_date_of_birth']
    )

    # Define columns for the report
    columns = [
        {"fieldname": "employee_name", "label": "Employee Name", "fieldtype": "Data", "width": 200, "class": "text-center"},
        {"fieldname": "formatted_date_of_birth", "label": "Date of Birth", "fieldtype": "Data", "width": 150},
        {"fieldname": "age", "label": "Age", "fieldtype": "Data", "width": 170},
        {"fieldname": "tenure", "label": "Working Tenure", "fieldtype": "Data", "width": 170},
        {"fieldname": "employment_status", "label": "Employee Status", "fieldtype": "Data", "width": 150},
        {"fieldname": "employee_code", "label": "Employee Code", "fieldtype": "Data", "width": 140},  
    ]

    return columns, report_data

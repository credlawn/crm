import frappe
from frappe.utils import getdate, today, date_diff
from calendar import month_name

def update_all_employee_age_and_tenure():
    employees = frappe.get_all("Employee", fields=["name", "date_of_birth", "joining_date", "last_working_date"])
    for employee_data in employees:
        employee = frappe.get_doc("Employee", employee_data.name)
        update_employee_fields(employee)

def update_employee_fields(employee):
    dob = getdate(employee.date_of_birth) if employee.date_of_birth else None
    joining_date = getdate(employee.joining_date)
    last_working_date = getdate(employee.last_working_date or today())

    if dob:
        age_years, age_months, age_days = calculate_age(dob)
        employee.age = f"{age_years} Years {age_months} Months"
        employee.birthday_month = month_name[dob.month]

    tenure_months, tenure_days = calculate_tenure(joining_date, last_working_date)
    employee.tenure = f"{tenure_months} Months {tenure_days} Days"
    
    employee.save()

def calculate_age(dob):
    today_date = getdate(today())
    years, months, days = today_date.year - dob.year, today_date.month - dob.month, today_date.day - dob.day
    if days < 0:
        months -= 1; days += (dob.replace(year=dob.year + 1, month=1, day=1) - dob.replace(year=dob.year, month=dob.month, day=1)).days
    if months < 0:
        years -= 1; months += 12
    return years, months, days

def calculate_tenure(joining_date, end_date):
    total_days = date_diff(end_date, joining_date)
    return total_days // 30, total_days % 30

@frappe.whitelist()
def scheduled_employee_update():
    update_all_employee_age_and_tenure()

import frappe
from frappe.model.document import Document
import re
from frappe.utils import nowdate

class CasePunching(Document):
    def validate(self):
        reference_pattern = r"^24[a-zA-Z]\d{2}[a-zA-Z]\d{8}[a-zA-Z0-9]{2}$"
        mobile_pattern = r"^\d{10}$"
        
        if self.reference_no:
            if not re.match(reference_pattern, self.reference_no):
                frappe.throw("Invalid Reference No. Please try again.")
            self.reference_no = str(self.reference_no)
            self.name = self.reference_no

        if not self.mobile_no:
            frappe.throw("Mobile Number is missing. Please enter a Mobile No.")
        elif not re.match(mobile_pattern, self.mobile_no):
            frappe.throw("Mobile Number must be 10 digits.")
        
        if self.customer_name:
            self.customer_name = self.customer_name.title().strip()

        if self.name:
            self.name = self.name.upper().strip()

    @frappe.whitelist()
    def after_insert(self):
        self.update_employee_name()

        # Match mobile_no with Calling Data
        self.match_mobile_no_in_calling_data()

    @frappe.whitelist()
    def on_update(self):
        self.update_employee_name()
        frappe.db.set_value("Case Punching", self.name, "update_date", nowdate())
        frappe.db.set_value("Case Punching", self.name, "update_time", frappe.utils.now())
        current_count = self.update_count or 0
        frappe.db.set_value("Case Punching", self.name, "update_count", current_count + 1)
        self.reload()
        
    def match_mobile_no_in_calling_data(self):
        calling_data = frappe.get_all("Calling Data", filters={"mobile_no": self.mobile_no}, fields=["employee_name"])

        if calling_data:
            frappe.db.set_value("Case Punching", self.name, "case_source", "App Data")
            frappe.db.set_value("Case Punching", self.name, "data_owner", calling_data[0].employee_name)
        else:
            frappe.db.set_value("Case Punching", self.name, "case_source", "Reference")

    def update_employee_name(self):
        employee = frappe.get_doc("Employee", self.employee_code)
        if employee:
            frappe.db.set_value("Case Punching", self.name, "employee_name", employee.employee_name)
            frappe.db.set_value("Case Punching", self.name, "email", employee.email)

        if not self.punching_date:
            frappe.db.set_value("Case Punching", self.name, "punching_date", nowdate())

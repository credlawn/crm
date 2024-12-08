from frappe.model.document import Document
import frappe



class CallingData(Document):    
    @frappe.whitelist()
    def after_insert(self):
        self.update_employee_name()

    @frappe.whitelist()
    def on_update(self):
        self.update_data_status()
        self.update_employee_name()
        self.reload()

    def update_employee_name(self):
        employee = frappe.get_doc("Employee", self.employee)
        if employee:
            frappe.db.set_value("Calling Data", self.name, "employee_name", employee.employee_name)
            frappe.db.set_value("Calling Data", self.name, "email", employee.email)

    def update_data_status(self):
        if self.lead_status in ["Not Interested", "Login Done", "Follow-up"]:
            frappe.db.set_value("Calling Data", self.name, "data_status", "Hold")



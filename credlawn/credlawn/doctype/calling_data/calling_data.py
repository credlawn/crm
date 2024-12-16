from frappe.model.document import Document
import frappe
from frappe.utils import now

class CallingData(Document):    
    def validate(self):
        if self.customer_name:
            self.customer_name = self.customer_name.title().strip()

    @frappe.whitelist()
    def after_insert(self):
        self.update_employee_name()

    @frappe.whitelist()
    def on_update(self):
        if self.is_new():
            return

        if self.has_value_changed("lead_status") and self.lead_status != "New Lead":
            self.update_date_and_count()
            self.save_update_date_to_fields()
            self.save_lead_status_to_fields()

        self.update_data_status()
        self.update_employee_name()

        if self.lead_status == "Login Done":
            self.create_case_punching_record()

        self.reload()

    def update_employee_name(self):
        employee = frappe.get_doc("Employee", self.employee) if self.employee else None
        if employee:
            frappe.db.set_value("Calling Data", self.name, "employee_name", employee.employee_name)
            frappe.db.set_value("Calling Data", self.name, "email", employee.email)
        else:
            frappe.db.set_value("Calling Data", self.name, "data_segment", "New")

    def update_data_status(self):
        if self.lead_status in ["Not Interested", "Login Done", "Follow-up"]:
            frappe.db.set_value("Calling Data", self.name, "data_status", "Hold")

    def update_date_and_count(self):
        if self.lead_status != "New Lead":
            frappe.db.set_value("Calling Data", self.name, "update_date", now())
            frappe.db.set_value("Calling Data", self.name, "update_time", frappe.utils.now())
            current_count = self.update_count or 0
            frappe.db.set_value("Calling Data", self.name, "update_count", current_count + 1)

    def save_update_date_to_fields(self):
        for i in range(1, 11):
            if not getattr(self, f"update_{i}"):
                frappe.db.set_value("Calling Data", self.name, f"update_{i}", now())
                break

    def save_lead_status_to_fields(self):
        for i in range(1, 11):
            if not getattr(self, f"status_{i}"):
                frappe.db.set_value("Calling Data", self.name, f"status_{i}", self.lead_status)
                break

    def create_case_punching_record(self):
        case_punching = frappe.get_doc({
            "doctype": "Case Punching",
            "customer_name": self.customer_name,
            "mobile_no": self.mobile_no,
            "employee_code": self.employee,
            "email": self.email,
        })

        if self.ip_status:
            case_punching.ip_status = self.ip_status
        if self.kyc_status:
            case_punching.kyc_status = self.kyc_status
        if self.incomplete_reason:
            case_punching.incomplete_reason = self.incomplete_reason
        if self.reference_no:
            case_punching.reference_no = self.reference_no
        if self.rejection_reason:
            case_punching.rejection_reason = self.rejection_reason

        case_punching.insert(ignore_permissions=True)

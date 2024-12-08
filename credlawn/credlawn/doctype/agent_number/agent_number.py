import frappe
from frappe.model.document import Document

class AgentNumber(Document):
    def before_insert(self):

        if self.agent_id:

            employee = frappe.get_doc("Employee", self.agent_id)

            if employee.mobile_no:
                self.mobile_no = "91" + str(employee.mobile_no).lstrip("91")

            if employee.employee_name:
            	self.agent_name = employee.employee_name


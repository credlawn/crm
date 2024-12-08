import frappe
from frappe.model.document import Document
from frappe.utils import getdate, nowdate

class Adobe(Document):

    def after_insert(self):
        self.update_fields()
        self.set_duplicate_finder()

    def on_update(self):
        self.update_fields()
        self.reload()

    def update_fields(self):
        if self.adobe_decision_date:
            day = self.get_adobe_decision_day()
            if day is not None:
                year, month = self.get_decision_month_year()
                final_decision_date = self.construct_date(year, month, day)
            else:
                final_decision_date = self.creation_date
        else:
            final_decision_date = self.creation_date
        
        frappe.db.set_value(self.doctype, self.name, 'final_decision_date', final_decision_date)

    def get_adobe_decision_day(self):
        if self.adobe_decision_date:
            try:
                if isinstance(self.adobe_decision_date, float):
                    day = int(self.adobe_decision_date)
                else:
                    day = int(str(self.adobe_decision_date).strip())
                    
                if 1 <= day <= 31:
                    return day
                else:
                    frappe.log_error("Invalid adobe_decision_date day", f"Adobe Decision Date must be between 1 and 31. Provided: {self.adobe_decision_date}")
            except ValueError:
                frappe.log_error("Invalid adobe_decision_date format", f"Adobe Decision Date must be a valid integer. Provided: {self.adobe_decision_date}")
        return None

    def get_decision_month_year(self):
        if self.decision_month:
            decision_month_date = getdate(self.decision_month)
            year = decision_month_date.year
            month = decision_month_date.month
            return year, month
        return None, None

    def construct_date(self, year, month, day):
        if year and month and day:
            return f"{year}-{month:02d}-{day:02d}"
        else:
            frappe.log_error("Invalid date construction", "Unable to construct a valid date from the provided data.")
            return None

    def set_duplicate_finder(self):
        customer_name = self.customer_name.strip() if self.customer_name else ""
        city = self.city.strip() if self.city else ""
        pin_code = str(self.pin_code).strip() if self.pin_code else ""
        
        duplicate_finder = f"{customer_name}{city}{pin_code}".lower().replace(' ', '')
        frappe.db.set_value(self.doctype, self.name, 'duplicate_finder', duplicate_finder)

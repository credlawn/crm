from frappe.model.document import Document
import frappe

class Cards(Document):
    def autoname(self):
        self.name = self.generate_card_code()

    def generate_card_code(self):
        existing_codes = self.get_existing_codes()
        next_code = self.get_next_code(existing_codes)
        return next_code

    def get_existing_codes(self):
        return [card.name for card in frappe.get_all('Cards', fields=['name'])]

    def get_next_code(self, existing_codes):
        if not existing_codes:
            return "aaaa"
        return self.increment_code(max(existing_codes))

    def increment_code(self, code):
        if code == "zzzz":
            return "aaaa"
        
        code_list = list(code)
        for i in reversed(range(len(code_list))):
            if code_list[i] == 'z':
                code_list[i] = 'a'
            else:
                code_list[i] = chr(ord(code_list[i]) + 1)
                return ''.join(code_list)

        return ''.join(code_list)

    def after_insert(self):
        self.change_case()

    def on_update(self):
        self.change_case()

    def change_case(self):
        if self.source == "Employee":
            self.sourcing_name = self.get_employee_name(self.sourced_by)
        elif self.source == "Vendor":
            self.sourcing_name = self.get_vendor_name(self.sourced_by)
        elif self.source == "Campaign":
            self.sourcing_name = self.get_campaign_name(self.sourced_by)

        if self.customer_name:
            self.customer_name = self.customer_name.title().strip()
        if self.pan_no:
            self.pan_no = self.pan_no.upper().strip()
        if self.city:
            self.city = self.city.title().strip()
        if self.email:
            self.email = self.email.lower().strip()

        fields_to_update = {
            'sourcing_name': self.sourcing_name,
            'customer_name': self.customer_name,
            'pan_no': self.pan_no,
            'city': self.city,
            'email': self.email
        }

        for field, value in fields_to_update.items():
            frappe.db.set_value('Cards', self.name, field, value)

    def get_employee_name(self, sourced_by):
        return frappe.get_value('Employee', {'name': sourced_by}, 'employee_name')

    def get_vendor_name(self, sourced_by):
        return frappe.get_value('Vendor', {'name': sourced_by}, 'vendor_name')

    def get_campaign_name(self, sourced_by):
        return frappe.get_value('Campaign', {'name': sourced_by}, 'campaign_name')

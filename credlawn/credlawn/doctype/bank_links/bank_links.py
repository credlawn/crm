import frappe
from frappe.model.document import Document

class BankLinks(Document):
    def before_insert(self):
        if self.dsa_code == "XCLW":
            if self.link_for == "Team":
                self.lc1_code = self.lc2_code = "CLWN21"
            elif self.link_for == "Campaign":
                self.lc1_code = self.lc2_code = "CIPL01"
            elif self.link_for == "Vendor":
                self.lc1_code = self.lc2_code = "CIPL02"
        
        if self.dsa_code == "XSBC":
            if self.link_for == "Team":
                self.lc1_code = self.lc2_code = "SBCL01"
            elif self.link_for == "Campaign":
                self.lc1_code = self.lc2_code = "SBCL02"
            elif self.link_for == "Vendor":
                self.lc1_code = self.lc2_code = "SBCL03"
        
        self.set_linkparts()

    def set_linkparts(self):
        partial_link = frappe.get_all('Partial Link', filters={'link_type': self.link_type}, fields=['linkpart1', 'linkpart2', 'linkpart3', 'linkpart4', 'linkpart5', 'linkpart6'])
        if partial_link:
            self.linkpart1 = partial_link[0].get('linkpart1', '')
            self.linkpart2 = partial_link[0].get('linkpart2', '')
            self.linkpart3 = partial_link[0].get('linkpart3', '')
            self.linkpart4 = partial_link[0].get('linkpart4', '')
            self.linkpart5 = partial_link[0].get('linkpart5', '')
            self.linkpart6 = partial_link[0].get('linkpart6', '')

    def after_insert(self):
        if self.link_type == "Normal":
            self.update_full_link_normal()
        elif self.link_type == "Tata":
            self.update_full_link_tata()
        elif self.link_type == "Swiggy":
            self.update_full_link_swiggy()
        elif self.link_type == "Marriott":
            self.update_full_link_marriott()

    def update_full_link_normal(self):
        # Replace lc2_code with '{}' if link_for is 'Campaign'
        lc2_code = '{}' if self.link_for == 'Campaign' else self.lc2_code or ''
        self.full_link = (
            f"{self.linkpart1 or ''}{self.dsa_code or ''}{self.linkpart2 or ''}"
            f"{self.sm_code or ''}{self.linkpart3 or ''}{self.lc1_code or ''}"
            f"{self.linkpart4 or ''}{lc2_code}{self.linkpart5 or ''}"
        )
        self.save()

    def update_full_link_tata(self):
        # Replace lc2_code with '{}' if link_for is 'Campaign'
        lc2_code = '{}' if self.link_for == 'Campaign' else self.lc2_code or ''
        self.full_link = (
            f"{self.linkpart1 or ''}{self.dsa_code or ''}{self.linkpart2 or ''}"
            f"{self.dsa_code or ''}{self.linkpart3 or ''}{self.lc1_code or ''}"
            f"{self.linkpart4 or ''}{lc2_code}{self.linkpart5 or ''}{self.sm_code or ''}"
        )
        self.save()

    def update_full_link_swiggy(self):
        # Replace lc2_code with '{}' if link_for is 'Campaign'
        lc2_code = '{}' if self.link_for == 'Campaign' else self.lc2_code or ''
        self.full_link = (
            f"{self.linkpart1 or ''}{self.dsa_code or ''}{self.linkpart2 or ''}"
            f"{self.dsa_code or ''}{self.linkpart3 or ''}{self.lc1_code or ''}"
            f"{self.linkpart4 or ''}{lc2_code}{self.linkpart5 or ''}{self.sm_code or ''}{self.linkpart6 or ''}"
        )
        self.save()

    def update_full_link_marriott(self):
        lc2_code = '{}' if self.link_for == 'Campaign' else self.lc2_code or ''
        self.full_link = (
            f"{self.linkpart1 or ''}{self.dsa_code or ''}{self.linkpart2 or ''}"
            f"{self.dsa_code or ''}{self.linkpart3 or ''}{self.lc1_code or ''}"
            f"{self.linkpart4 or ''}{lc2_code}{self.linkpart5 or ''}{self.sm_code or ''}{self.linkpart6 or ''}"
        )



        self.save()

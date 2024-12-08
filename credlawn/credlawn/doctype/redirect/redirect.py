import frappe
from frappe.model.document import Document
import requests
from user_agents import parse

class Redirect(Document):
    def before_insert(self):
        self.click_count = 1
        self.device, self.browser = self.get_device_browser_info(self.user_agent or "Mozilla/5.0")
        self.city = self.get_ip_info(self.ip_address)
        self.set_click_type(self.ip_address, self.source)

    def get_ip_info(self, ip_address):
        access_token = self.get_ipinfo_access_token()
        if access_token:
            ip_info = requests.get(f"https://ipinfo.io/{ip_address}/json?token={access_token}").json()
            city = ip_info.get("city", "Unknown")
            region = ip_info.get("region", "Unknown")
            return f"{city} - {region}" if city != "Unknown" and region != "Unknown" else "Unknown"
        return "Unknown"

    def get_ipinfo_access_token(self):
        access_token_record = frappe.get_doc('Access Tokens', 'ipinfo.io')
        access_token = access_token_record.get_password("access_token")
        return access_token if access_token else None

    def get_device_browser_info(self, user_agent_string):
        user_agent = parse(user_agent_string)
        os = user_agent.os.family
        device = "Android" if "Android" in os else "iOS" if "iOS" in os else "Mac OS" if "Mac" in os else "Windows" if "Windows" in os else "Android" if "Linux" in os else "Unknown"
        return device, user_agent.browser.family

    def set_click_type(self, ip_address, source):
        self.click_type = "Repeat" if frappe.db.exists("Redirect", {"ip_address": ip_address, "source": source}) else "New"

    def after_insert(self):
        # Exclude based on source or browser containing 'bot', 'BOT', or 'Bot'
        excluded_sources = ['hdfc', 'tata', 'swiggy', 'campt', 'camph', 'camps']
        if self.source.startswith('CRLAWN/'):
            self.source = self.source[len('CRLAWN/'):]
        if any(excluded_source.lower() in self.source.lower() for excluded_source in excluded_sources) or 'bot' in self.browser.lower():
            return
        
            
        
        
        blasting = frappe.get_all('Blasting', filters={'link': self.source}, fields=['name'])
        if blasting:
            blasting_doc = frappe.get_doc('Blasting', blasting[0].name)
            blasting_doc.cr_date = self.timestamp
            blasting_doc.save()

            click_fields = ['click_1', 'click_2', 'click_3', 'click_4', 'click_5', 'click_6', 'click_7', 'click_8']
            for click_field in click_fields:
                if not getattr(blasting_doc, click_field):
                    setattr(blasting_doc, click_field, self.timestamp)
                    blasting_doc.save()
                    break

        else:
            frappe.get_doc({
                'doctype': 'Blasting',
                'link': self.source,
                'cr_date': self.timestamp,
                'click_1': self.timestamp,
                'lead_type': 'Click',
                'city': self.city
            }).insert()

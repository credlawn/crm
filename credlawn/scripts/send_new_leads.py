import frappe
import time
import requests
from frappe.utils import today

@frappe.whitelist()
def send_leads():

    frappe.enqueue('credlawn.scripts.send_new_leads.send_leads_async', queue='long', timeout=3600, is_async=True)

def send_leads_async():


    blasting_docs = frappe.get_all('Blasting', filters={'lead_assigned': 'No'}, fields=['name', 'customer_name', 'mobile_no', 'link', 'whatsapp_account'])

    # Fetch agent numbers where 'allow_lead' = 'Yes'
    agent_numbers = frappe.get_all('Agent Number', filters={'allow_lead': 'Yes'}, fields=['agent_id', 'mobile_no', 'agent_name'])

    if not agent_numbers:
        frappe.log_error("No agents found with 'allow_lead' = 'Yes'.", "Agent Number Error")
        return

    for idx, blasting_doc in enumerate(blasting_docs):
        blasting_doc_details = frappe.get_doc('Blasting', blasting_doc.name)
        
        agent = agent_numbers[idx % len(agent_numbers)]  # Distribute leads in round-robin fashion


        send_whatsapp_message(blasting_doc_details, agent)


        time.sleep(60)

def send_whatsapp_message(blasting_doc, agent):
    customer_name = blasting_doc.customer_name
    mobile_no = blasting_doc.mobile_no
    link = "https://cipl.me/" + blasting_doc.link
    whatsapp_account = blasting_doc.whatsapp_account
    agent_number = agent['mobile_no']
    agent_name = agent['agent_name']
    assigned_date = today()

    credlawn_record = frappe.get_doc('Credlawn Whatsapp', whatsapp_account)
    phone_no_id = credlawn_record.phone_no_id
    access_token = credlawn_record.get_password("access_token")
    template_name = credlawn_record.template_name

    # Prepare the message data
    data = {
        "messaging_product": "whatsapp",
        "to": agent_number, 
        "type": "template",
        "template": {
            "name": template_name,
            "language": {
                "code": "en"
            },
            "components": [
                {
                    "type": "header",
                    "parameters": [
                        {
                            "type": "text",
                            "text": customer_name
                        }
                    ]
                },
                {
                    "type": "body",
                    "parameters": [
                        {
                            "type": "text",
                            "text": customer_name
                        },
                        {
                            "type": "text",
                            "text": mobile_no
                        },
                        {
                           "type": "text",
                            "text": link
                        }
                    ]
                }
            ]
        }
    }


    response = requests.post(
        f'https://graph.facebook.com/v20.0/{phone_no_id}/messages',
        headers={
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        },
        json=data
    )


    if response.status_code == 200:

        frappe.db.set_value('Blasting', blasting_doc.name, 'lead_assigned', 'Yes')
        frappe.db.set_value('Blasting', blasting_doc.name, 'agent_number', agent_number)
        frappe.db.set_value('Blasting', blasting_doc.name, 'agent_name', agent_name)
        frappe.db.set_value('Blasting', blasting_doc.name, 'assigned_date', assigned_date)
        frappe.db.commit()
    else:
        frappe.log_error(f"Failed to send message for {blasting_doc.name} to agent {agent['agent_name']} ({agent['mobile_no']}). Error: {response.text}")
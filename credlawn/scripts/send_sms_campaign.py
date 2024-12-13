import frappe
import requests
import time

def get_access_token():
    try:
        access_token_record = frappe.get_doc('Access Tokens', 'msg91')
        access_token = access_token_record.get_password("access_token")
        if access_token:
            return access_token
        else:
            frappe.throw("Access token not found.")
    except Exception as e:
        frappe.log_error(f"Error fetching access token: {str(e)}", "get_access_token")
        return None

def create_recipient_data(record, campaign_doc):
    recipient_data = {
        "mobiles": record.mobile_no
    }
    for var_name, var_value in [
        (record.var_1_name, record.var_1_value),
        (record.var_2_name, record.var_2_value),
        (record.var_3_name, record.var_3_value),
        (record.var_4_name, record.var_4_value),
    ]:
        if var_name and var_value:
            recipient_data[var_name] = var_value
    return recipient_data

@frappe.whitelist()
def send_sms(campaign_name):
    frappe.enqueue(
        'credlawn.scripts.send_sms_campaign.send_sms_async',
        campaign_name=campaign_name,
        queue='long',
        timeout=3600,
        is_async=True
    )

def send_sms_async(campaign_name):
    camp_data_records = frappe.get_all('Campaigndata', filters={'parent': campaign_name}, fields=[
        'name', 'template_id', 'mobile_no', 'var_1_name', 'var_1_value', 'var_2_name', 'var_2_value',
        'var_3_name', 'var_3_value', 'var_4_name', 'var_4_value', 'campaign_date', 'message_status',
        'sms_response', 'sms_sent_timestamp', 'sms_error_message'
    ])

    if not camp_data_records:
        return "failure"

    campaign_doc = frappe.get_doc('Campaign', campaign_name)
    access_token = get_access_token()
    if not access_token:
        return "failure"

    url = "https://control.msg91.com/api/v5/flow"
    headers = {
        'accept': 'application/json',
        'authkey': access_token,
        'content-type': 'application/json'
    }

    batch_size = 60
    recipient_batch = []
    successful_records = []

    for i, record_data in enumerate(camp_data_records):
        try:
            # Fetch the full Campaigndata document for each record
            record = frappe.get_doc('Campaigndata', record_data.name)
            if not record:
                continue

            recipient_data = create_recipient_data(record, campaign_doc)
            recipient_batch.append(record)  # Store the actual document, not a dict

            if len(recipient_batch) == batch_size or i == len(camp_data_records) - 1:
                data = {
                    "template_id": record_data.template_id,
                    "short_url": "0",
                    "realTimeResponse": "1",
                    "recipients": [create_recipient_data(r, campaign_doc) for r in recipient_batch]  # Use document data
                }

                response = requests.post(url, headers=headers, json=data)

                if response.status_code == 200:
                    successful_records.extend([r.name for r in recipient_batch])  # Now `r` is the actual document

                    update_query = """
                        UPDATE `tabCampaigndata`
                        SET message_status = 'Sent',
                            sms_response = %s,
                            sms_sent_timestamp = %s
                        WHERE name IN (%s)
                    """
                    params = (response.text, frappe.utils.now(), "', '".join([r.name for r in recipient_batch]))
                    frappe.db.sql(update_query, params)

                    recipient_batch = []
                    time.sleep(1)
                else:
                    error_message = f"Error: {response.status_code} - {response.text}"
                    update_query = """
                        UPDATE `tabCampaigndata`
                        SET sms_response = %s,
                            sms_error_message = %s
                        WHERE name IN (%s)
                    """
                    params = (response.text, error_message, "', '".join([r.name for r in recipient_batch]))
                    frappe.db.sql(update_query, params)

                    frappe.log_error(f"Error sending SMS. Response: {response.text}", "send_sms_async")

        except Exception as e:
            frappe.log_error(f"Error while processing recipient {record_data.name}: {frappe.get_traceback()}", "Error while sending SMS")

    if successful_records:
        try:
            successful_records_str = "', '".join(successful_records)
            query = f"""
                UPDATE `tabCampaigndata`
                SET message_status = 'Sent'
                WHERE name IN ('{successful_records_str}')
            """
            frappe.db.sql(query)
            frappe.db.commit()
        except Exception as e:
            frappe.log_error(f"Error while bulk updating message status: {str(e)}", "send_sms_async")
    return "success"        

 






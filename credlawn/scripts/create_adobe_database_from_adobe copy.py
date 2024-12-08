import frappe
from frappe.model.document import Document

def update_adobe_database_records():
    adobe_records = frappe.get_all('Adobe', fields=['name', 'reference_no', 'customer_name', 'creation_date', 'customer_type', 
                                                    'sm_code', 'product_code', 'promo_code', 'lc1_code', 'company_name', 
                                                    'dropoff_reason', 'idcom_status', 'vkyc_status', 'ipa_status', 
                                                    'current_status', 'city', 'state', 'pin_code', 'surrogate_eligibility', 
                                                    'decline_code', 'final_decision', 'etb_nb_succ_flag', 'curable_flag', 
                                                    'decline_description', 'channel', 'kyc_type', 'vkyc_expire_date', 
                                                    'vkyc_link', 'dap_final_flag', 'lc2_code', 'lg_code', 'restart_flag', 
                                                    'qde_status', 'company_code', 'dsa_code', 'inprocess_classification', 
                                                    'classification', 'decline_type', 'bkyc_status', 'bkyc_status_reason', 
                                                    'login_month', 'decision_month', 'duplicate_finder', 'file_type', 
                                                    'adobe_decision_date', 'final_decision_date', 'decision_date'])

    for adobe in adobe_records:
        reference_no = adobe['reference_no']

        try:
            # Check if the record with the same reference_no exists in Adobe Database
            existing_record = frappe.db.get_value('Adobe Database', {'reference_no': reference_no}, ['name', 'decision_date'])

            # Prepare data for updating or creating the record
            update_data = {}
            change_log = []

            decision_date = adobe.get('decision_date')  # Get decision_date from Adobe doctype
            final_decision_date = adobe.get('final_decision_date')  # Get final_decision_date

            for field in ['promo_code', 'decline_description', 'decline_code', 'bkyc_status', 'product_code', 
                          'bkyc_status_reason', 'vkyc_link', 'vkyc_expire_date', 'vkyc_status', 'kyc_type', 
                          'dap_final_flag', 'qde_status', 'dropoff_reason', 'current_status', 'customer_name', 
                          'creation_date', 'customer_type', 'sm_code', 'lc1_code', 'company_name', 'idcom_status', 
                          'ipa_status', 'city', 'state', 'pin_code', 'surrogate_eligibility', 'final_decision', 
                          'etb_nb_succ_flag', 'curable_flag', 'channel', 'lc2_code', 'lg_code', 'restart_flag', 
                          'company_code', 'dsa_code', 'inprocess_classification', 'classification', 'decline_type', 
                          'login_month', 'decision_month', 'duplicate_finder', 'file_type', 'adobe_decision_date', 
                          'final_decision_date']:
                value = adobe.get(field)
                if value:
                    # Compare the existing value with the new value
                    if existing_record:
                        old_value = frappe.db.get_value('Adobe Database', existing_record, field)
                        if old_value != value:
                            # Log the change in the desired format
                            change_log.append(f"{field.replace('_', ' ').title()}: {old_value} --> {value}")
                            update_data[field] = value
                    else:
                        update_data[field] = value

            if existing_record:
                # Update the existing record in Adobe Database if there are changes
                if change_log:
                    change_log.append(f"\nDecision Date: {final_decision_date}")  # Add blank line before decision_date
                    frappe.db.set_value('Adobe Database', existing_record, 'change_log', "\n".join(change_log))
                    frappe.db.set_value('Adobe Database', existing_record, update_data)

            else:
                # If record doesn't exist, create a new one in Adobe Database
                new_data = {"reference_no": adobe.get('reference_no')}
                new_data.update(update_data)

                doc = frappe.get_doc({
                    "doctype": "Adobe Database",
                    **new_data
                })

                if change_log:
                    change_log.append(f"\nDecision Date: {final_decision_date}")  # Add blank line before decision_date
                    doc.change_log = "\n".join(change_log)

                doc.insert()

        except Exception as e:
            # Log the error for the current record and continue with the next one
            frappe.log_error(message=str(e), title=f"Error syncing record {reference_no}")
            continue

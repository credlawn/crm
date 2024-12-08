import frappe
import pandas as pd

def process_adobe_dump_email(doc):
    if "adobe dump" in doc.subject.lower():
        attachments = frappe.get_all("File", filters={"attached_to_doctype": "Communication", "attached_to_name": doc.name})
        file_records = []

        for attachment in attachments:
            file_record = frappe.get_doc("File", attachment.name)
            if file_record.file_name.endswith('.xlsx'):
                file_records.append(file_record)

        if file_records:
            if process_excel_attachment(file_records[0].name):
                frappe.delete_doc("Communication", doc.name)
                for file_record in file_records:
                    frappe.delete_doc("File", file_record.name)

def process_excel_attachment(file_name):
    file_doc = frappe.get_doc("File", file_name)
    file_content = file_doc.get_content()

    if not file_content:
        return False

    try:
        data = pd.read_excel(file_content)
    except Exception as e:
        frappe.log_error(f"Error reading Excel file: {str(e)}")
        return False

    records_to_insert = []
    for _, row in data.iterrows():
        records_to_insert.append({
            'doctype': 'Adobe',
            'reference_no': row.get('APPLICATION_REFERENCE_NUMBER', 'Not Mapped') if pd.notna(row.get('APPLICATION_REFERENCE_NUMBER')) else None,
            'customer_name': row.get('CUSTOMER_NAME', 'Not Mapped') if pd.notna(row.get('CUSTOMER_NAME')) else None,
            'creation_date': row.get('CREATION_DATE', 'Not Mapped') if pd.notna(row.get('CREATION_DATE')) else None,
            'customer_type': row.get('CUSTOMER_TYPE', 'Not Mapped') if pd.notna(row.get('CUSTOMER_TYPE')) else None,
            'sm_code': row.get('SM_CODE', 'Not Mapped') if pd.notna(row.get('SM_CODE')) else None,
            'product_code': row.get('PRODUCT_CODE', 'Not Mapped') if pd.notna(row.get('PRODUCT_CODE')) else None,
            'lc1_code': row.get('LC1_CODE', 'Not Mapped') if pd.notna(row.get('LC1_CODE')) else None,
            'company_name': row.get('COMPANY_NA', 'Not Mapped') if pd.notna(row.get('COMPANY_NA')) else None,
            'dropoff_reason': row.get('DROPOFF_REASON', 'Not Mapped') if pd.notna(row.get('DROPOFF_REASON')) else None,
            'idcom_status': row.get('IDCOM_STATUS', 'Not Mapped') if pd.notna(row.get('IDCOM_STATUS')) else None,
            'promo_code': row.get('PROMO_CODE', 'Not Mapped') if pd.notna(row.get('PROMO_CODE')) else None,
            'ipa_status': row.get('IPA_STATUS', 'Not Mapped') if pd.notna(row.get('IPA_STATUS')) else None,
            'current_status': row.get('CURRENT_ST', 'Not Mapped') if pd.notna(row.get('CURRENT_ST')) else None,
            'city': row.get('CITY', 'Not Mapped') if pd.notna(row.get('CITY')) else None,
            'state': row.get('STATE', 'Not Mapped') if pd.notna(row.get('STATE')) else None,
            'vkyc_status': row.get('VKYC_STATU', 'Not Mapped') if pd.notna(row.get('VKYC_STATU')) else None,
            'surrogate_eligibility': row.get('SURROGATE_ELIGIBILITY', 'Not Mapped') if pd.notna(row.get('SURROGATE_ELIGIBILITY')) else None,
            'decline_code': row.get('DECLINE_CODE', 'Not Mapped') if pd.notna(row.get('DECLINE_CODE')) else None,
            'final_decision': row.get('FINAL_DECISION', 'Not Mapped') if pd.notna(row.get('FINAL_DECISION')) else None,
            'etb_nb_succ_flag': row.get('ETB_NB_SUCC_FLAG', 'Not Mapped') if pd.notna(row.get('ETB_NB_SUCC_FLAG')) else None,
            'pin_code': row.get('PIN_CODE', 'Not Mapped') if pd.notna(row.get('PIN_CODE')) else None,
            'decline_description': row.get('DECLINE_DESCRIPTION', 'Not Mapped') if pd.notna(row.get('DECLINE_DESCRIPTION')) else None,
            'channel': row.get('CHANNEL', 'Not Mapped') if pd.notna(row.get('CHANNEL')) else None,
            'kyc_type': row.get('VKYC_CONSENT_DATE', 'Not Mapped') if pd.notna(row.get('VKYC_CONSENT_DATE')) else None,
            'vkyc_expire_date': row.get('VKYC_EXPIR', 'Not Mapped') if pd.notna(row.get('VKYC_EXPIR')) else None,
            'curable_flag': row.get('CURABLE_FLAG', 'Not Mapped') if pd.notna(row.get('CURABLE_FLAG')) else None,
            'dap_final_flag': row.get('DAP_FINAL_FLAG', 'Not Mapped') if pd.notna(row.get('DAP_FINAL_FLAG')) else None,
            'lc2_code': row.get('LC2_CODE', 'Not Mapped') if pd.notna(row.get('LC2_CODE')) else None,
            'lg_code': row.get('LG_CODE', 'Not Mapped') if pd.notna(row.get('LG_CODE')) else None,
            'restart_flag': row.get('RESTART_FLAG', 'Not Mapped') if pd.notna(row.get('RESTART_FLAG')) else None,
            'vkyc_link': row.get('CAPTURE_LINK', 'Not Mapped') if pd.notna(row.get('CAPTURE_LINK')) else None,
            'company_code': row.get('COMPANY_CODE', 'Not Mapped') if pd.notna(row.get('COMPANY_CODE')) else None,
            'dsa_code': row.get('VARIABLE_VALUE', 'Not Mapped') if pd.notna(row.get('VARIABLE_VALUE')) else None,
            'adobe_decision_date': row.get('FINAL_DECISION_DATE', 'Not Mapped') if pd.notna(row.get('FINAL_DECISION_DATE')) else None,
            'qde_status': row.get('QDE_STATUS', 'Not Mapped') if pd.notna(row.get('QDE_STATUS')) else None,
            'decline_type': row.get('Decline Type', 'Not Mapped') if pd.notna(row.get('Decline Type')) else None,
            'bkyc_status': row.get('BKYC Status', 'Not Mapped') if pd.notna(row.get('BKYC Status')) else None,
            'bkyc_status_reason': row.get('BKYC Status Reason', 'Not Mapped') if pd.notna(row.get('BKYC Status Reason')) else None,
            'inprocess_classification': row.get('Inprocess Classification', 'Not Mapped') if pd.notna(row.get('Inprocess Classification')) else None,
            'classification': row.get('Classification', 'Not Mapped') if pd.notna(row.get('Classification')) else None,
            'login_month': row.get('LOGIN_MONTH', 'Not Mapped') if pd.notna(row.get('LOGIN_MONTH')) else None,
            'decision_month': row.get('DECISION_M', 'Not Mapped') if pd.notna(row.get('DECISION_M')) else None
        })

    # Insert all records at once
    if records_to_insert:
        try:
            for record in records_to_insert:
                frappe.get_doc(record).insert()
            frappe.db.commit()
            return True
        except Exception as e:
            frappe.log_error(f"Error inserting records: {str(e)}")
    return False

def execute_email_processing():
    try:
        latest_comm = frappe.get_all("Communication", filters={"subject": ["like", "%Adobe Dump%"]}, order_by="creation desc", limit=1)
        if latest_comm:
            process_adobe_dump_email(frappe.get_doc("Communication", latest_comm[0].name))
    except Exception as e:
        frappe.log_error(f"Error processing email: {str(e)}")

def enqueue_email_processing():
    frappe.enqueue(execute_email_processing, queue="default", timeout=3000, is_async=True)
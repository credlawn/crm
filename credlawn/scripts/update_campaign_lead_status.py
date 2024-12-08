import frappe
import time

@frappe.whitelist()
def update_status():
    calling_data_records = frappe.db.sql("""
        SELECT mobile_no, lead_status, modified
        FROM `tabCalling Data`
    """, as_dict=True)

    case_punching_records = frappe.db.sql("""
        SELECT mobile_no, ip_status, update_date
        FROM `tabCase Punching`
    """, as_dict=True)

    for record in calling_data_records:
        blasting = frappe.db.sql("""
            SELECT name, lead_status, status_update_date
            FROM `tabBlasting`
            WHERE mobile_no = %s
        """, (record['mobile_no']), as_dict=True)

        if blasting:
            blasting_doc = blasting[0]
            if blasting_doc['lead_status'] == "IP Approved":
                continue

            update_needed = False

            if blasting_doc['lead_status'] != record['lead_status']:
                update_needed = True
                frappe.db.sql("""
                    UPDATE `tabBlasting`
                    SET lead_status = %s
                    WHERE name = %s
                """, (record['lead_status'], blasting_doc['name']))

            if update_needed:
                frappe.db.sql("""
                    UPDATE `tabBlasting`
                    SET status_update_date = %s
                    WHERE name = %s
                """, (record['modified'], blasting_doc['name']))
                
                frappe.db.commit()

        time.sleep(0.1)

    for record in case_punching_records:
        blasting = frappe.db.sql("""
            SELECT name, lead_status, status_update_date
            FROM `tabBlasting`
            WHERE mobile_no = %s
        """, (record['mobile_no']), as_dict=True)

        if blasting:
            blasting_doc = blasting[0]
            if blasting_doc['lead_status'] == "IP Approved":
                continue

            update_needed = False

            if blasting_doc['lead_status'] != record['ip_status']:
                update_needed = True
                frappe.db.sql("""
                    UPDATE `tabBlasting`
                    SET lead_status = %s
                    WHERE name = %s
                """, (record['ip_status'], blasting_doc['name']))

            if update_needed:
                frappe.db.sql("""
                    UPDATE `tabBlasting`
                    SET status_update_date = %s
                    WHERE name = %s
                """, (record['update_date'], blasting_doc['name']))
                
                frappe.db.commit()

        time.sleep(0.1)

@frappe.whitelist()
def enqueue_update_status():
    frappe.enqueue(update_status, queue='long')

import frappe

@frappe.whitelist()
def update_file_type():
    records = frappe.get_all('Adobe', fields=['name', 'duplicate_finder', 'dap_final_flag'])
    grouped_records = {}
    
    # Group records by 'duplicate_finder'
    for record in records:
        df_value = record['duplicate_finder']
        if df_value not in grouped_records:
            grouped_records[df_value] = []
        grouped_records[df_value].append(record)

    # Process each group
    for df_value, group in grouped_records.items():
        # Check if the group has only one record (Single) or more (Multi)
        file_type = 'Single' if len(group) == 1 else 'Multi'
        
        # For each record, check dap_final_flag to determine if it's Complete or Incomplete
        for record in group:
            if str(record['dap_final_flag']).strip().lower() == 'yes':
                frappe.db.set_value('Adobe', record['name'], 'file_type', f'{file_type} Complete')
            else:
                frappe.db.set_value('Adobe', record['name'], 'file_type', f'{file_type} Incomplete')

    frappe.db.commit()
    frappe.msgprint("File types updated successfully.")

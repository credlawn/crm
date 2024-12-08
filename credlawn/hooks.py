app_name = "credlawn"
app_title = "Credlawn"
app_publisher = "Credlawn India Private Limited"
app_description = "CRM"
app_email = "info@credlawn.com"
app_license = "mit"





app_include_css = [
    "/assets/credlawn/css/credlawn.css" 
]

webhooks = [
    {
        "method": "POST",
        "url": "/api/method/credlawn.webhook.sms_delivery_report.get_sms_delivery_report"
    }
]



scheduler_events = {
    "cron": {
        "0 0 * * *": [  # This runs every day at midnight
            "credlawn.scripts.update_employee_age_n_tenure.scheduled_employee_update"
        ],
        "0 * * * *": [  # This runs every hour
            "credlawn.scripts.email_processing.enqueue_email_processing",
            "credlawn.scripts.clean_redirect_link.delete_redirect_link",
            "credlawn.scripts.delete_bot_click_entry.delete_bot_click_records",
            "credlawn.scripts.find_duplicate_in_adobe.update_file_type",
            "credlawn.scripts.create_adobe_database_from_adobe.update_adobe_database_records",
            "credlawn.scripts.fetch_mobile_no_from_svkyc_link.process_svkyc_link_records",
            "credlawn.scripts.map_employee_in_approved_dump.enqueue_update_sourced_by"
        ],

        "*/10 * * * *": [  # This runs every 10 minutes
            "credlawn.scripts.update_campaign_lead_status.update_status"
        ],


        "*/5 * * * *": [  # This runs every 5 minutes
            "credlawn.scripts.send_new_leads.send_leads"
        ]
    }
}












# scheduler_events = {
# 	"all": [
# 		"credlawn.tasks.all"
# 	],
# 	"daily": [
# 		"credlawn.tasks.daily"
# 	],
# 	"hourly": [
# 		"credlawn.tasks.hourly"
# 	],
# 	"weekly": [
# 		"credlawn.tasks.weekly"
# 	],
# 	"monthly": [
# 		"credlawn.tasks.monthly"
# 	],
# }


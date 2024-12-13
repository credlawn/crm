frappe.ui.form.on('Campaign', {
    setup(frm) {
        frappe.realtime.on('campaign_insert_progress', (data) => {
            if (data.campaign !== frm.doc.name) return;

            let percent = Math.floor((data.current * 100) / data.total);
            let seconds = Math.floor(data.eta);
            let minutes = Math.floor(data.eta / 60);
            let eta_message = 
                seconds < 60
                    ? __('About {0} seconds remaining', [seconds])
                    : minutes === 1
                    ? __('About {0} minute remaining', [minutes])
                    : __('About {0} minutes remaining', [minutes]);

            let message = __("Creating Short Link {0} of {1}, {2}", [data.current, data.total, eta_message]);

            frm.dashboard.show_progress(__('Campaign Insertion Progress'), percent, message);

            if (data.current === data.total) {
                frm.dashboard.show_progress(__('Campaign Insertion Progress'), 100, __("{0} out of {1} Link created successfully", [data.total, data.total]));

                
                if (frm.page) {
                    frm.page.set_indicator(__('Completed'), 'green');
                }

                setTimeout(() => {
                    frm.dashboard.hide();
                    frm.reload_doc();
                }, 5000);
            } else {
                if (frm.page) {
                    frm.page.set_indicator(__('In Progress'), 'orange');
                }
            }
        });
    },

    refresh: function(frm) {
        frm.page.hide_icon_group();
        frm.trigger("update_indicators");


        if (!frm.is_local && frm.doc.campaign_type === 'SMS' && frm.doc.campaign_status == 'Created') {
            if (!frm.__is_reload_done) {
                frm.__is_reload_done = true;

                frm.add_custom_button(__('Run Campaign'), function() {
                    frappe.confirm(
                        __('Are you sure you want to run this campaign?'),
                        function() {
                            frappe.call({
                                method: "credlawn.scripts.send_sms_campaign.send_sms",
                                args: { "campaign_name": frm.doc.name }
                            });
                            frappe.msgprint(__('Campaign Started in Background'));
                        },
                        function() {
                            frappe.msgprint(__('Campaign run canceled.'));
                        }
                    );
                });
            }
        }
    }
});

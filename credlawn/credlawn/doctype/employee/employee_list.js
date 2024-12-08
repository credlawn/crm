frappe.listview_settings['Employee'] = {
    onload: function(listview) {
        // Hide the sidebar
        $('.layout-side-section').hide();
        $('.layout-main-section-wrapper, .layout-main-section').css('margin-left', '0');
        $('.page-container').addClass('no-sidebar');   
        
    }
};

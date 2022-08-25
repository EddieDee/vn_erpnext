frappe.ui.form.on('Sales Invoice', {
//     refresh(frm){
//     frappe.show_alert('Refreshed');
//   } ,
//   validate(){
//       frappe.show_alert('validated')
//   },
    setup(frm) {
        frm.add_fetch('customer', 'customer_type', 'customer_type');
        frm.add_fetch('customer', 'tax_id_type', 'tax_id_type');
    },
	onload(frm) {
		// your code here
		console.log('Initial script ',frm);
		if (frm.doc.is_return == 1) {
            /* Auto fetch ncf for the first sales invoice and make generate ncf read only in case of return */
            cur_frm.set_value('generate_ncf', 0);
            cur_frm.set_df_property('generate_ncf', 'read_only', true);
            cur_frm.add_fetch('return_against', 'ncf', 'ncf');
            cur_frm.refresh_field('ncf');
            cur_frm.refresh_fields();
        }
	},
	before_cancel(frm) {
         if(frm.doc.docstatus==1 && !!frm.timeline.get_communication_timeline_contents().length){
            frappe.throw(__("Comenta la razon antes de cancelar."));
            frappe.validated = false; 
        }
    },
    customer(frm) {
	console.log(frm.doc.customer);
	frm.add_fetch('customer', 'customer_type', 'customer_type');
        if (frm.doc.is_pos){
                var pos_profile = frm.doc.pos_profile;
        }
        const customer = frm.doc.customer;
        if( frappe.user_roles.includes('Accounts Manager') && customer){
            frm.set_value('generate_ncf', 1);
            // frm.set_df_property('generate_ncf', 'read_only', true)
                
        } else {
            frm.set_value('generate_ncf', 1);
            frm.set_df_property('generate_ncf', 'read_only', true);
        }
    },
    //     console.log('Customer is: ', customer)
    //     if (customer) {
    //         frappe.call({
    //             method: 'frappe.client.get_value',
    //             freeze: true,
    //             async: true,
    //             args: {
    //                 doctype: 'Customer',
    //                 filters: { name: customer },
    //                 fieldname: ['customer_type'],
    //             },callback(r) {
    //                  if (!r.exc) {
    //                      console.log('no se log que es')
                     
    //                     // console.log('callback data: ', r)
    //                     // const tax_id = r.message.tax_id
    //                     const customer_type = r.message.customer_type
    //                     // por si el otro var de arriba no funciona... TODO
    //                     // cur_frm.set_value('tax_id', tax_id)
    //                     frm.set_value('customer_type', customer_type)
    //                     // por si el otro var de arriba no funciona... TODO
    //                     frm.set_value('tax_id_type', customer_type)
    //                     if( frappe.user_roles.includes('Accounts Manager') && customer && customer_type){
    //                         frm.set_value('generate_ncf', 1);
    //                         // frm.set_df_property('generate_ncf', 'read_only', true)
                            
    //                     } else {
    //                         frm.set_value('generate_ncf', 1);
    //                         frm.set_df_property('generate_ncf', 'read_only', true)
    //                     }
    //                  }
    //             }
    //         })
    //     }
    // },
    before_save(frm) {
        if (flt(frm.doc.grand_total) <= 0) {
            frappe.msgprint("Debes agregar por lo menos un articulo para crear una factura.");
            frappe.validated = false;
        }
    },
    after_cancel(frm) {
        // console.log("Cancelled");
        frm.set_df_property('generate_ncf', 'read_only', false);
        cur_frm.set_value('generate_ncf', 0);
        
    },
    
});

// frappe.provide('erpnext');
// require

frappe.ui.form.on('Sales Invoice', {
    // //    get_fields.prototype= {
        //     // const me = this;
        //     setup:function(frm){
            //   console.log('testing....');
            //     }
            //     });
            
// {% include 'erpnext/selling/page/point_of_sale/point_of_sale.js' %};
onload: function(frm){
console.log('Fuera del metodo');
}
})
// var g_ncf_chk = frappe.ui.form.make_control({
//     df: {
//         fieldname: 'g_ncf',
//         fieldtype: 'Check',
//         label: __('Comprobante Fiscal'),
        
//     },
//     parent: this.wrapper.find('.cart-container'),
//     render_input: true,
// });

// frappe.ui.form.on('Sales Invoice', {
//     //    get_fields.prototype= {
//         // const me = this;
//       setup:function(frm){
//         console.log('estamos dentro....');
//         }
//         });

// function test(p1,p2){
//     console.log('estamos dentro');
//     console.log(p1+p2);
    
// };
// test(4,8);
            
// frappe.provide("erpnext.accounts");
// erpnext.accounts.SalesInvoiceController = erpnext.selling.SellingController.extend({
// 	setup: function(doc) {
// 		this.setup_posting_date_time_check();
//         this._super(doc);
//         console.log('avanzando...');
        
//         console.log(cur_dialog.paid_amount);
//         console.log(doc);
        

//     },
// });
# -*- coding: utf-8 -*-

{
    'name': 'crm and sale ext',
    'summary': 'Crm and Sale Ext',
    'description': """
        Crm and Sale Ext
       
    """,
    'version': '1.0.13',
    'category': 'CRM',
    'author': 'Numan.',
    'support': 'a',
    'website': 'https://www.almightycs.com',
    'license': 'OPL-1',
    'depends': ['base', 'sale'],
    'data': [
        "security/ir.model.access.csv",
        "view/sale_view.xml",
        "view/commission_report.xml",

    ],

    'installable': True,
    'application': True,
    'sequence': 1,
    'price': 36,
    'currency': 'USD',
}

#   Disclaimer: We Collect following information for analytics and improving our product/services.
#   Number of Users, Patients, Dr, Appointments, Prescriptions, Laboratory, Radiology, 
#       Surgery, Hospitalization and other medical records (Only Count)
#   Company Name, List of installed modules, DB key, email, mobile and url (to match customer data to update details.)
#   Only if related modules are installed those data will be fetched.
#   We do not sale this information or pulish customer details anywhere without having approval from customer
#   This same detail get used for our monthly subscription users also.
#   Privay Policy: https://www.almightycs.com/privacy-policy

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

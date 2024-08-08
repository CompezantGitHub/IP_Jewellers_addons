# -*- coding: utf-8 -*-
{
    'name': "IP Jewellery Master By Compezant",

    'summary': """This will create Jewellery Master by compezant for IP Jewellers""",

    'description': """
       This will create Jewellery Master by compezant
    """,

    'author': "Compezant Software Solution",
    'website': "https://www.Compezant.com",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','product','website_sale', 'website_sale_stock', 'website_sale_wishlist','website_sale_comparison','loyalty', 'sale_loyalty','website_payment', 'website_mail', 'portal_rating', 'digest', 'delivery'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/purity_unit_views.xml',
        'views/stone_master_views.xml',
        'views/metal_master_views.xml',
        'views/jewellery_master_view.xml',
        'views/discount_master_view.xml',
        'views/sku_code_template.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'icon': "/your_module_name/static/description/icon.png",
    "images": ["/static/description/banner.png"],
    "license": "OPL-1",
    "price": 0,
    "currency": "EUR",
}

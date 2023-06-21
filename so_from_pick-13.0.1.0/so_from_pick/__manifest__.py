# -*- coding: utf-8 -*-

{   
    'name': 'Create Sale order from Picking & Delivery Order & Incoming Shipment',
    'version': '1.0',
    'category': 'website',
    'license': 'OPL-1',
    'summary': """Create sale order from delivery order & picking & incoming shipment""", 
    'description': """


        so from picking & delivery order
        sale from picking & delivery order
        create so from picking & delivery order
        create sale from picking & delivery order
        create sale order from picking & delivery order
        picking & delivery order to sale
        picking & delivery order to so 
        one click so generate
        picking & delivery order to so automation

        so from picking & incoming shipment
        sale from picking & incoming shipment
        create so from picking & incoming shipment
        create sale from picking & incoming shipment
        create sale order from picking & incoming shipment
        picking & incoming shipment to sale
        picking & incoming shipment to so 
        one click so generate
        picking & incoming shipment to so automation
        
        

    """,  
    'depends': ['sale_stock'],    
    'data' : [
        'view/picking.xml',
    ],
    
    'images': ['static/description/main_screen.png'],      
    'author': 'Craftsync Technologies',
    'website': 'https://www.craftsync.com',
    'maintainer': 'Craftsync Technologies',
    'installable': True,
    'currency': 'EUR',
    'price': 14.99,
    'auto_install': False,
    'application': True,
          
}

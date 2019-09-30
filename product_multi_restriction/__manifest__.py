{
    'name': 'Product Multi Restriction',
    'category': 'Product',
    'summary': 'Product Multi Restriction',
    'description' : '''Product Multi Restriction''',
    'depends': ['sale_management', 'sale_stock', 'purchase', 'mrp'],
    'data': [
        'views/product_views.xml',
    ],
    'application': True,
    'installable': True,
}
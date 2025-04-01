{
    'name': "Carte de visite", 
    'version': '1.0',  
    'depends': ['base'],  
    'author': "Siby&Aliou",  
    'category': 'Tools',  
    'description': """
    Gestion des cartes de visites
    """, 

    'data': [
        
        'security/ir.model.access.csv', 
        'views/qr_views.xml',
        'views/menu_qr_views.xml', 

  
    ],

    'demo': [
        # Ajoute ici tes démonstrations si nécessaire
    ],



    'license': 'LGPL-3',

}

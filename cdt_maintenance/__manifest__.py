{
    "name": "CDT Maintenance",
    "version": "18.0.1.0.0",
    "summary": "Maintenance et installation d'equipements industriels du CDT",
    "category": "Services",
    "author": "Urie",
    "license": "LGPL-3",
    "depends": ["base", "mail", "contacts", "maintenance", "stock", "purchase", "project", "calendar"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "data/sequences.xml",
        "views/equipement_views.xml",
        "views/demande_views.xml",
        "views/intervention_views.xml",
    ],
    "installable": True,
    "application": True,
}
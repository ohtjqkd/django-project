from django.apps import AppConfig
import json, os

class PortfolioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'portfolio'
    static_datasource = json.loads(open('./portfolio/datasource.json').read())

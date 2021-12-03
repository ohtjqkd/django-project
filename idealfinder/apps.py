from django.apps import AppConfig


class IdealfinderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'idealfinder'
    template_path = 'idealfinder/'
    static_path = 'idealfinder/'

class HomeConfig(IdealfinderConfig):
    template = 'index.html'
    css = 'index.css'
    api='/'

class ProcessReponse(IdealfinderConfig):
    tempalte = 'process_response.html'
    
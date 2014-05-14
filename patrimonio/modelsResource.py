#-*- encoding:utf-8 -*-
from import_export import fields
from import_export import resources

from utils.functions import formata_moeda
from models import *

class PatrimonioResource(resources.ModelResource):
    class Meta:
        model = Patrimonio

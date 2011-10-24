# -*- coding: utf-8 -*-

from django.db import models
import time
# Create your models here.

DIA = 60*60*24
SEMANA = DIA*7
MES = DIA*30
ANO = DIA*365

class Link(models.Model):
    descricao = models.CharField(max_length=60)
    roteador = models.IntegerField()
    porta = models.CharField(max_length=50)
    inverter = models.BooleanField(u'Inverter entrada e saída?', default=False)
    fechado = models.BooleanField(u'Link fechado?', default=False)
    
    def agora(self):
        return int(time.time())

    def dia(self):
    	return self.agora()-DIA

    def semana(self):
    	return self.agora()-SEMANA

    def mes(self):
        return self.agora()-MES

    def ano(self):
    	return self.agora()-ANO

    def __unicode__(self):
    	return self.descricao

    def portas(self):
        return self.porta.split('+')

    def aggr(self):
        if len(self.portas()) > 1:
	   return True
	else: return False

    def t1(self):
        if self.inverter:
	   return 'Out'
	else: return 'In'

    def t2(self):
        if self.inverter:
	   return 'In'
	else: return 'Out'

from django.db import models

# Create your models here.

class BlocoIP(models.Model):
    ip = models.IPAddressField()
    mask = models.IntegerField()
    entidade = models.ForeignKey('identificacao.Entidade', limit_choices_to={'asn__isnull':False})
    obs = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return '%s/%s' % (self.ip, self.mask)
    __unicode__.admin_order_field = 'ip'

    def AS(self):
        return self.entidade.asn
    AS.short_description = 'AS'

    class Meta:
        verbose_name = u'Bloco IP'
        verbose_name_plural = u'Blocos IP'
        ordering = ('entidade__sigla',)

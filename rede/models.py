from django.db import models

# Create your models here.

class BlocoIP(models.Model):
    ip = models.IPAddressField()
    mask = models.IntegerField()
    asn = models.ForeignKey('identificacao.ASN')
    superbloco = models.ForeignKey('rede.BlocoIP', null=True, blank=True, verbose_name='Super bloco')
    designado = models.ForeignKey('identificacao.Entidade', null=True, blank=True)
    rir = models.ForeignKey('rede.RIR', null=True, blank=True)
    obs = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return '%s/%s' % (self.ip, self.mask)
    __unicode__.admin_order_field = 'ip'

    class Meta:
        verbose_name = u'Bloco IP'
        verbose_name_plural = u'Blocos IP'
        ordering = ('asn__entidade__sigla',)


class RIR(models.Model):
    nome = models.CharField(max_length=40)

    def __unicode__(self):
        return self.nome


class Provedor(models.Model):
    ip = models.IPAddressField()
    mask = models.IntegerField()
    provedor = models.CharField(max_length=40)

    def __unicode__(self):
        return self.provedor

class Rota(models.Model):
    aspath = models.CharField(u'AS path', max_length=255)
    blocoip = models.ForeignKey('rede.BlocoIP', verbose_name='Bloco IP')
    nexthop = models.IPAddressField()
    provedor = models.ForeignKey('rede.Provedor')
    preferencial = models.BooleanField()
    local_pref = models.IntegerField(null=True, blank=True)
    historico = models.ForeignKey('rede.Historico')

    def __unicode__(self):
        return '%s %s' % (self.historico, self.blocoip)

class Historico(models.Model):
    arquivo = models.FileField(upload_to='rede')
    horario = models.DateTimeField(auto_now=True)
    equipamento = models.ForeignKey('patrimonio.Patrimonio', null=True, blank=True)


    def __unicode__(self):
        return self.horario

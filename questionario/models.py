# -*- coding: utf-8 -*-
from django.db import models

CARGO = (
    (1, u'Diretor/Gerente'),
    (2, u'Analista'),
    (3, u'Técnico'),
    (4, u'Outros'),
)

RESPOSTAS = (
    (1, u'Discordo totalmente'),
    (2, u'Discordo parcialmente'),
    (3, u'Não concordo nem discordo'),
    (4, u'Concordo parcialmente'),
    (5, u'Concordo totalmente'),
)

class Questionario(models.Model):
      pergunta1 = models.IntegerField(u'1. Minha função/cargo atual que exerço é de', choices=CARGO)
      pergunta2 = models.IntegerField(u'2. Minha função tem ligação direta/indireta com a segurança da informação', choices=RESPOSTAS)
      pergunta3 = models.IntegerField(u'3. Conheço o documento que trata da Política de Segurança da Informação adotada pela organização', choices=RESPOSTAS)
      pergunta4 = models.IntegerField(u'4. Sou informado quando ocorrem mudanças na Política de Segurança da Informação', choices=RESPOSTAS)
      pergunta5 = models.IntegerField(u'5. Segurança da Informação é um item importante para os negócios desenvolvidos na organização', choices=RESPOSTAS)
      pergunta6 = models.IntegerField(u'6. Conheço os procedimentos de cópias de segurança adotados pela organização (Ex: freqüência de geração, tipo de backup, etc)', choices=RESPOSTAS)
      pergunta7 = models.IntegerField(u'7. Atualmente, o método utilizado para a realização de cópias de segurança atende as necessidades da organização', choices=RESPOSTAS)
      pergunta8 = models.IntegerField(u'8. As cópias de segurança realizadas pela organização contêm informações suficientes para restaurar um sistema de informação a um estado recente, operável, e preciso', choices=RESPOSTAS)
      pergunta9 = models.IntegerField(u'9. A freqüência de geração das cópias de segurança reflete os requisitos de negócio', choices=RESPOSTAS)
      pergunta10 = models.IntegerField(u'10. O período de armazenamento das informações esta determinado', choices=RESPOSTAS)
      pergunta11 = models.IntegerField(u'11. As cópias de segurança são armazenadas em ambientes distintos dos sistemas de origem', choices=RESPOSTAS)
      pergunta12 = models.IntegerField(u'12. As cópias de segurança que são mantidas em outros ambientes são protegidas contra acesso não autorizado', choices=RESPOSTAS)
      pergunta13 = models.IntegerField(u'13. São realizados cópias de segurança de dados sensíveis', choices=RESPOSTAS)
      pergunta14 = models.IntegerField(u'14. As cópias de segurança são criptografadas, tanto na execução quanto em seu armazenamento', choices=RESPOSTAS)
      pergunta15 = models.IntegerField(u'15. São mantidos registros precisos e completos das cópias de segurança realizadas', choices=RESPOSTAS)
      pergunta16 = models.IntegerField(u'16. As cópias de segurança são periodicamente testadas para garantir que elas são suficientemente confiáveis para o uso de emergência', choices=RESPOSTAS)
      pergunta17 = models.IntegerField(u'17. Existe um ambiente separado para testar os procedimentos de restauração do sistema', choices=RESPOSTAS)
      pergunta18 = models.IntegerField(u'18. Existe um procedimento escrito e atualizado para a realização das cópias de segurança', choices=RESPOSTAS)
      pergunta19 = models.IntegerField(u'19. Este procedimento escrito contém instruções para tratamento de erros ou outras condições excepcionais', choices=RESPOSTAS)
      pergunta20 = models.IntegerField(u'20. Este procedimento escrito contém dados para contatos de suporte para o caso de eventos operacionais inesperados ou dificuldades técnicas', choices=RESPOSTAS)

      def __unicode__(self):
          return u'Questionário número %s' % self.id



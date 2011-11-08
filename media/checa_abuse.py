# -*- coding: utf-8 -*-

import imaplib
import email
import csv
import subprocess
import time
import re
from email.header import decode_header
from django.core.mail import send_mail
from django.core.management import setup_environ
import settings
setup_environ(settings)
from abuse.models import *
from datetime import datetime

IGUAIS = {'unip.br': 'unip-objetivo.br'}
TIPOS = {'Spam':['spam'], 'Malware':['infectado', 'bot', 'malware', 'malicioso'],'Scan':['varredura'],'Ataque':[],'Outros':[], 'Copyright':['BayTSP']}

def decoded(s):
    ret = []
    for t in decode_header(s):
        if t[1] is not None:
           ret.append(t[0].decode(t[1]))
        else:
           ret.append(t[0])
    return ' '.join(ret)


def find_code(s, cods):
    for c in cods:
        if s.find(c) > -1:
           return c
    return None

def process_whois(ip):
    
    email = None
    owner = None
    emails = []
    cods = []
    atual = None
    print ip
    output = subprocess.Popen(['/usr/bin/whois', '-h', 'whois.lacnic.net', ip], stdout=subprocess.PIPE).communicate()[0]

    for d in output.split('\n'):
        c = find_code(d, cods)
        if d.startswith('owner:'):
            lixo, owner = d.split(':')
        elif d.startswith('owner-c:') or d.startswith('tech-c:'):
            x, cod = d.split(':')
            cods.append(cod.strip())
        elif atual and d.startswith('e-mail:'):
            x, email = d.split(':')
            emails.append(email.strip())
        elif c:
            atual = c

    return (owner, emails)

tabela = {}
def tabela_whois(ip):
    if tabela.has_key(ip):
        return tabela.get(ip)

    time.sleep(10)
    o,e = process_whois(ip)
    tabela[ip] = (o,e)
    return (o,e)

falta_env = []
falta_class = []
terminado = {}
ips = {}

def termina(data, num):
                        data_msg = datetime.strptime(data, '%d-%b-%Y %H:%M:%S +0000')
                        mes = data_msg.strftime('%b-%Y')
                        if terminado.has_key(mes):
                            terminado[mes].append(num)
                        else:
                            terminado[mes] = [num]

def processa_email(ip, msg, tipo, num, ass):
                    if ip in ips.keys(): 
                        ips[ip] += 1
                        termina(date[1], num)
                        return
                    (owner, emails) = tabela_whois(ip)
                    ips[ip] = 1
                    import string
                    receberam = map(string.strip, decoded(msg['To']).split(',') + decoded(msg['CC']).split(','))
                    enviado = False
                    if tipo and owner:
                        owner = owner.decode('cp1252').strip()
                        try:
                            inst = Instituicao.objects.get(nome=owner)
                        except Instituicao.DoesNotExist:
                            inst = Instituicao(nome=owner)
                            inst.save()
                        mens = Mensagem()
                        mens.assunto = ass
                        mens.instituicao = inst
                        mens.tipo = tipo
                        mens.ip = ip
                        mens.quantidade = 1
                        mens.data = datetime.strptime(date[1], '%d-%b-%Y %H:%M:%S +0000')
                        mens.save()
                        fc = False
                    else:
                        fc = True
               
                    receberam = [r.split('@')[1].lower() for r in receberam if r != 'None']
                    rec = []
                    for r in receberam:
                        if r in IGUAIS.keys():
                            rec.append(IGUAIS[r])
                        rec.append(r)
                    receberam = rec
                    emails2 = [e.split('@')[1].lower() for e in emails]
                    print receberam, emails2
                    em = []
                    for e in emails2:
                        if e in IGUAIS.keys():
                            em.append(IGUAIS[e])
                        em.append(e)
                    emails2 = em
                    for e in emails2:
                        if e in receberam:
                            enviado = True
                            break
                    if not enviado and emails:
                        #print 'send mail'
                        send_mail('Não é mais teste - emails abuse', 'E-mail com assunto %s precisaria ser enviado para %s, mas só foi enviado para %s' % (ass, str(receberam), str(emails)), 'abuse@ansp.br', ['antonio@ansp.br', 'carlos@ansp.br'], fail_silently=False)
                    fe = False
                    if not enviado and not emails:
                        fe = True

	            print fc, fe, enviado, emails2, receberam, tipo, ass
               
                    if fe and fc:
                        pass
                    elif fe:
                        falta_env.append(num)
                    elif fc:
                        falta_class.append(num)
                    else:
                        termina(date[1], num)

endereco = 'nara@ansp.br'
senha = 'Seg!@nsp'
#senha = 'Jus+Test'
saida = open('/tmp/mails.teste', 'w')
errors = open('/tmp/mails.errors', 'w')
M = imaplib.IMAP4_SSL('imap.gmail.com')
M.login(endereco, senha)
M.select()
typ, data = M.search(None, '(UNSEEN)')

for num in data[0].split():
    typ, data = M.fetch(num, '(RFC822 INTERNALDATE)')
    date = data[1].split('"')
    msg = email.message_from_string(data[0][1])            

    corpo = msg.get_payload(decode=True)
    ass = decoded(msg['Subject'])

    tipo = None
    for t in Tipo.objects.all():
        if not corpo: corpo = ''
        if not ass: ass = ''
        for p in t.palavras_chave.split():
            if corpo.find(p.encode('ascii')) > -1 or ass.find(p.encode('ascii')) > -1:
               tipo = t
               break
        if tipo: break

    frm = msg['From']
    #print frm
    if frm.find('@cais.rnp.br') > 0:

    	mail = re.split('----------------------------------+', str(msg))


    	if len(mail) > 1:
       	    if mail[1].find('|') > -1:
                delim = '|'
            else:
                delim = ','
            csv_data = [x.rstrip() for x in mail[1].split('\n')]
            reader = csv.reader(csv_data, delimiter=delim)
            i = -1
            for l in reader:
                print l
                if len(l) == 0: continue
                if i > -1:
                    if i >= len(l): continue
                    processa_email(l[i], msg, tipo, num,ass)

                for j in range(len(l)):
                    if l[j].startswith('IP'):
                        i = j
                        break
           
        else:
             print "%s -> nada" % num

    elif frm.find('@copyright-compliance.com') > 0:
        ip = str(msg).split('Infringers IP Address:')
        if len(ip) > 1:
            ip = ip[0].lstrip()
            ip = ip.split()[0]
            processa_email(ip, msg, tipo, num, ass)



env = ','.join(falta_env)
if env:
    result = M.copy(env, 'falta enviar')
    if result[0] == 'OK':
        M.store(env, '+FLAGS', '(\Deleted)')
        M.expunge()

classf = ','.join(falta_class)
if classf:
    result = M.copy(classf, 'falta classificar')
    if result[0] == 'OK':
        M.store(classf, '+FLAGS', '(\Deleted)')
        M.expunge()

for mes in terminado.keys():
    term = ','.join(terminado[mes])
    if term:
        M.create(mes.lower())
        result = M.copy(term, mes.lower())
        if result[0] == 'OK':
            M.store(term, '+FLAGS', '(\Deleted)')
            M.expunge()
    

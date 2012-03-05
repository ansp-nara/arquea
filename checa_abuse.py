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

def process_whois(ip, lacnic=True):
    
    email = None
    owner = None
    emails = []
    cods = []
    atual = None
    print ip
    if ip == '200.136.76.10': return (None, None)
    lac_list = ['-h', 'whois.lacnic.net'] if lacnic else []
    output = subprocess.Popen(['/usr/bin/whois'] + lac_list + [ip], stdout=subprocess.PIPE).communicate()[0]

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
    if not o: o,e = process_whois(ip, False)
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
                            if num not in terminado[mes]:
                                terminado[mes].append(num)
                        else:
                            terminado[mes] = [num]

def processa_email(ip, msg, tipo, num, ass, cont, lista=None):
                    if ip in ips.keys(): 
                        ips[ip] += 1
                        return cont
                    (owner, emails) = tabela_whois(ip)
                    print owner
                    import string
                    receberam = map(string.strip, decoded(msg['To']).split(',') + decoded(msg['CC']).split(','))
                    enviado = False
                    if tipo and owner:
                        ips[ip] = 1
                        owner = owner.decode('cp1252').strip()
                        try:
                            inst = Instituicao.objects.get(nome=owner)
                        except Instituicao.DoesNotExist:
                            inst = Instituicao(nome=owner)
                            inst.save()
                        mens = Mensagem()
                        mens.assunto = ass[:99]
                        mens.instituicao = inst
                        mens.tipo = tipo
                        mens.ip = ip
                        mens.quantidade = 1
                        mens.data = datetime.strptime(date[1], '%d-%b-%Y %H:%M:%S +0000')
                        if lista is not None:
                            lista.append(mens)
                        else:
                            mens.save()
                            termina(date[1], num)
 			cont += 1
                        print 'Mais um: %s\n' % cont
                    else: print "Não leu do whois %s\n\n\n\n\n\n\n\n" % ip

                    return cont

endereco = 'teste.ansp@gmail.com'
#senha = 'Seg!@nsp'
senha = 'Jus+Test'
saida = open('/tmp/mails.teste', 'w')
errors = open('/tmp/mails.errors', 'w')
M = imaplib.IMAP4_SSL('imap.gmail.com')
M.login(endereco, senha)
M.select()
typ, data = M.search(None, '(UNSEEN)')
cont = 0

for num in data[0].split():
    typ, data = M.fetch(num, '(RFC822 INTERNALDATE)')
    date = data[1].split('"')
    msg = email.message_from_string(data[0][1])            

    corpo = msg.get_payload(decode=True)
    ass = decoded(msg['Subject'])
    ips = {}

    tipo = None
    for t in Tipo.objects.order_by('id'):
        if not corpo: corpo = ''
        if not ass: ass = ''
        for p in t.palavras_chave.split():
            if corpo.find(p.encode('ascii')) > -1 or ass.find(p.encode('ascii')) > -1:
               tipo = t
               break
        if tipo: break

    if not tipo: tipo = Tipo.objects.get(nome='Outros')

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
            chamadas = cont
            lista = []
            for l in reader:
                print l
                if len(l) == 0: continue
                if i > -1:
                    if i >= len(l): continue
                    cont = processa_email(l[i], msg, tipo, num,ass, cont, lista)
                    print lista

                for j in range(len(l)):
                    if l[j].startswith('IP'):
                        i = j
                        break

            if (cont - chamadas) == len(lista):
                [mens.save() for mens in lista]
                termina(date[1],num)
           
        else:
             print "%s -> nada" % num

    elif frm.find('@copyright-compliance.com') > 0:
        ip = str(msg).split('Infringers IP Address:')
        if len(ip) > 1:
            ip = ip[1].lstrip()
            ip = ip.split()[0]
            print ip
            cont = processa_email(ip, msg, tipo, num, ass, cont)

    elif frm.find('@reports.spamcop.net') > 0:
        ip = str(msg).split('Email from')
        if len(ip) > 1:
           ip = ip[1].lstrip()
           ip = ip.split()[0]
           print ip
           cont = processa_email(ip, msg, tipo, num, ass, cont)

    elif str(msg).find('@gte.net') > 0:
        ip = ass.split()[-1]
        print ip
        cont = processa_email(ip, msg, tipo, num, ass, cont)


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
    

#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.core.management import setup_environ
import settings
setup_environ(settings)
inicio = 2008
fim = 2011

from django.db import connection

cursor = connection.cursor()

cursor.execute("select id, first_name, last_name from auth_user where id < 25 order by first_name")
users = cursor.fetchall()
dados = {}
for u in users:
    dd = []
    for t in range(inicio, fim+1):
        query = "select count(*) from django_admin_log where user_id=%s and action_flag=%s and action_time >= '%s-01-01' and action_time < '%s-01-01'" 
        cursor.execute(query % (u[0], 1, t, t+1))
        ad = cursor.fetchone()[0]
        cursor.execute(query % (u[0], 2, t, t+1))
        mod = cursor.fetchone()[0]
        cursor.execute(query % (u[0], 3, t, t+1))
        de = cursor.fetchone()[0]

        dd.append({'ano': t, u'inclusões': ad, u'modificações': mod, u'exclusões': de})
    dados['%s %s' % u[1:]] = dd

users = dados.keys()
users.sort()
for u in users:
    print u
    for d in dados[u]:
        print '    %s  %4s  %4s  %4s' % (d['ano'], d[u'inclusões'], d[u'modificações'], d[u'exclusões'])

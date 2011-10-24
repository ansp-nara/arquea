#!/usr/bin/python

from django.core.management import setup_environ
import settings
setup_environ(settings)

from sys import path

path.append('/var/lib/admin')

tipos = (14,13,19,18,16,17)

from django.db import connection, transaction
cursor = connection.cursor()

for tp in tipos:
    cursor.execute("select content_type_id, object_id from django_admin_log where user_id=24 and content_type_id=%s" % tp)

    objects = cursor.fetchall()
    erros = 0
    for o in objects:
        cursor.execute("select app_label, model from django_content_type where id=%s" % o[0])
        m = cursor.fetchone()
        try:
	   if tp == 13:
	       cursor.execute("delete from protocolo_itemprotocolo where protocolo_id=%s" % o[1])
	       transaction.commit_unless_managed()

           cursor.execute("delete from %s_%s where id=%s" % (m[0], m[1], o[1]))
	   transaction.commit_unless_managed()

        except Exception, e:
           erros += 1
           print "Erro %s - %s" % (erros, e)
	

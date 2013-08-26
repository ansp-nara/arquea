#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.core.management import setup_environ
import settings
setup_environ(settings)

from django.contrib.admin.models import LogEntry

years= range(2008,2013)
years.reverse()
users = LogEntry.objects.values_list('user', flat=True).order_by().distinct()

for year in years:
    print year
    print
    print '%15s | %40s | %05s | %05s | %05s' % ('user', 'nome', 'add', 'mod', 'del')
    ano = LogEntry.objects.filter(action_time__year=year)
    for u in users:
        logs = ano.filter(user__id=u)
        if logs:
            user = logs[0].user.username
            nome = '%s %s' % (logs[0].user.first_name, logs[0].user.last_name)
            add = logs.filter(action_flag=1).count()
            change = logs.filter(action_flag=2).count()
            delete = logs.filter(action_flag=3).count()
            print '%15s | %40s | %5d | %5d | %5d' % (user,nome,add,change,delete)
    print
    print

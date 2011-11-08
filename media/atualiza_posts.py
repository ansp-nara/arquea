#!/usr/bin/python

from django.core.management import setup_environ
import settings
setup_environ(settings)
from intranet.models import LatestPosts, Reuniao


LatestPosts.atualiza(10,5)
Reuniao.atualiza()


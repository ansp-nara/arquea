# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm

def release_perform():
    result = prompt("Fechar versão master do sistema? [yes/No]:")
    if result and result.upper() in ['YES', 'Y']:
        local("prerelease")
        local("release")
        local("postrelease")

def restart_apache_dev():
    sudo("service apache2 restart")
    
def deploy_dev():
    # prepara diretório para o checkout do SVN
    result = run("rm -r /home/rogerio/sistema-exp/*")
    run("rmdir /home/rogerio/sistema-exp")
    
    
    ## NESTE PONTO PODIAMOS FAZER LOCALMENTE O CHECKOUT 
    ## E ENVIAR UM TAR.GZ PARA O SERVIDOR
    ## RESTRINGINDO O ACESSO DO SERVIDOR WEB AO SERVIDOR SVN
    
    # Checkout completo do SVN
    run("svn export https://www.ansp.br/svn/sistema /home/rogerio/sistema-exp")
    
    # copiando todos os arquivos do SVN para o sistema
    run("cp -rf /home/rogerio/sistema-exp/* /var/lib/sistema")
    # copiando os arquivos staticfiles
    sudo ("python /var/lib/sistema/manage.py collectstatic --settings=sistema.prod")

    # parando o apache para modificar os arquivos do sistema
    sudo("service apache2 stop")

    # removendo os arquivos python binários, para não ter problema com arquivos removidos
    run("rm -rf /var/lib/sistema/*.pyc")
    
    # reiniciando o apache
    sudo("service apache2 start")

    
    
"""
 Definição da localização dos arquivos no Subversion para uso na task de deploy
 
 Uso:
     fab master
     fab branch
     fab branch:1.1.1
"""
def master():
    branch('trunk')
    
def branch(branchname=None):
    if branchname == None:
        local("svn list https://www.ansp.br/svn/poc-projeto-python/src/tags/")
        
        branchname = prompt("Digite o numero da tag:", default='trunk')
    if branchname != 'trunk':
        #local("svn list https://www.ansp.br/svn/poc-projeto-python/src/tags/%s" % branchname)
        env.branch = "https://www.ansp.br/svn/poc-projeto-python/src/tags/%s" % branchname
    else:
        #local("svn list https://www.ansp.br/svn/poc-projeto-python/src/trunk/")
        env.branch = "https://www.ansp.br/svn/poc-projeto-python/src/trunk/"

"""
 Definição da localização do host, do servidor web do django.
 O usuáriorio deve digitar a senha de acesso.
 
 Uso:
     fab dev
     fab production
"""
def dev():
    env.hosts = ['10.0.0.23']
    env.user = 'rogerio'
    

    
"""
 Definição da task de deploy. 
 Depende da definição da localização do subversion. [master, branch]
 Depende da definição da localização do host. [dev, production]

"""
def deploy():
    if not hasattr(env, 'branch'):
        branch()

    print 'Teste deploy.'
    print 'Baixando arquivos de %s' % env.branch
    run('uname -s')

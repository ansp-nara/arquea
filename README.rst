============
Sistema ANSP
============

Sistema de gerenciamento de projetos Fapesp desenvolvido pelo NARA/ANSP.
É um conjunto de aplicações Django para gerenciar concessões e gastos de
um projeto Fapesp.

Instalação
..........

1. Instale os pacotes de desenvolvimento do ``python``, ``xml``, ``ffi`` e ``xslt`` ``zlib`` e ``yaml``. No caso do Ubuntu, seria::

    apt-get install libffi-dev libpython-dev libxml2-dev libxslt1-dev zlib1g-dev libyaml-dev

2. Instale o ``django-sistema``::

    pip install --extra-index-url http://10.0.1.65/simple/ django-sistema

Configuração
............

1. Crie um novo projeto Django::

    django-admin startproject <nome do projeto>


2. Adicione os apps ao ``INSTALLED_APPS`` no seu ``settings.py``::

    INSTALLED_APPS = (
        'configuracao',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'carga',
        'evento',
        'financeiro',
        'identificacao',
        'membro',
        'memorando',
        'monitor',
        'outorga',
        'patrimonio',
        'pesquisa',
        'processo',
        'protocolo',
        'rede',
        'verificacao',
        'repositorio',
        'utils',
        'ckeditor',
        'tinymce',
        'import_export',
        'treemenus',
        'menuextension',
        ...
    )


   Note que o app "configuracao" deve ser o primeiro da lista.
   Os cinco últimos apps da lista são apps adicionais.

3. Inclua em ``MIDDLEWARE_CLASSES`` no seu ``settings.py``::

    MIDDLEWARE_CLASSES = (
        ...
        'utils.request_cache.RequestCacheMiddleware',
    )

4. Inclua em ``TEMPLATE_CONTEXT_PROCESSORS`` no seu ``settings.py``::

    TEMPLATE_CONTEXT_PROCESSORS = (
        'django.contrib.auth.context_processors.auth',
        'django.core.context_processors.debug',
        'django.core.context_processors.i18n',
        'django.core.context_processors.media',
        'django.core.context_processors.static',
        'django.core.context_processors.request',
        'django.contrib.messages.context_processors.messages',
        ...
        'utils.context_processors.applist',
        'utils.context_processors.debug',
        'utils.context_processors.papelaria',
    )

5. Inclua a seguinte configuração do ckeditor ao seu ``settings.py``::

    CKEDITOR_UPLOAD_PATH = 'ckeditor/'

6. Inclua a seguinte configuração para os arquivos estáticos em seu ``settings.py``::

    STATIC_ROOT = '<caminho completo>'

7. Inclua as urls do apps no ``urls.py`` do seu projeto::

    from django.views.generic import TemplateView

    urlpatterns = patterns('',
        ...
        (r'^files/(?P<filename>.*)', 'utils.views.serve_files'),
        (r'^protocolo/', include('protocolo.urls')),
        (r'^patrimonio/', include('patrimonio.urls')),
        (r'^financeiro/', include('financeiro.urls')),
        (r'^outorga/', include('outorga.urls')),
        (r'^memorando/', include('memorando.urls')),
        (r'^monitor/', include('monitor.urls')),
        (r'^identificacao/', include('identificacao.urls')),
        (r'^membro/', include('membro.urls')),
        (r'^rede/', include('rede.urls')),
        (r'^processo/', include('processo.urls')),
        (r'^verificacao/', include('verificacao.urls')),
        (r'^repositorio/', include('repositorio.urls')),
        (r'^carga/', include('carga.urls')),
        (r'^configuracao/', include('configuracao.urls')),
        (r'^verifica$', 'utils.views.verifica'),
        (r'^sempermissao$', TemplateView.as_view(template_name="401.html")),
        (r'^tinymce/', include('tinymce.urls')),
        (r'^ckeditor/', include('ckeditor.urls')),
        (r'^', include(admin.site.urls)),
    )

   A primeira url é utilizada para que o django verifique permissões antes que um arquivo
   seja baixado.
   A última faz com que a home do projeto seja a home do admin.

8. Entre no diretório do seu projeto e execute
   ::

    python manage.py migrate

   para criar a base de dados inicial e
   ::

    python manage.py loaddata initial_data.yaml

   para carregar os dados iniciais.

9. Execute
   ::

    python manage.py createsuperuser

   para criar o super usuário inicial.

10. Execute
    ::

     python manage.py runserver

    e acesse http://localhost:8080 para verificar se a aplicação está rodando.

11. Estando tudo ok nas etapas anteriores, é hora de colocar em produção. Abaixo, é utilizado o Apache + WSGI, mas
pode ser feito de outras maneiras, como descrito em https://docs.djangoproject.com/en/1.7/howto/deployment/ .

    a. Instale o ``apache2``, o ``mod_wsgi`` e o ``mod_xsendfile``;
    b. Habilite esses módulos;
    c. Configure o apache. Considerando que o sistema rodará sozinho na máquina, a configuração seria apenas
       modificar o arquivo ``/etc/apache2/sites-available/000-default``::


        XSendFile on
        XSendFilePath /var/www
        XSendFileUnescape on

        WSGIPythonPath /project/path

        <VirtualHost *:80>
            ...

            Alias /static/ /var/www/static/

            <Directory /var/www/static>
                Require all granted
            </Directory>

            WSGIScriptAlias / /project/path/project/wsgi.py
            <Directory /project/path/project>
                <Files wsgi.py>
                    Require all granted
                </Files>
            </Directory>

            ...
        </VirtualHost>

    d. Execute, no diretório do projeto::

        python manage.py collectstatic


Apêndice
--------

Talvez não seja simples instalar o mod_xsendfile. No Ubuntu, por exemplo, a versão empacotada é desatualizada, e não
faz URL encoding, o que faz com que não suporte caracteres não ASCII no nome do arquivo.  Por isso, é recomendável
instalar a versão mais recente disponível em https://tn123.org/mod_xsendfile/. Faça o download da versão ``tar.gz`` ou
``tar.bz2``. Instale o pacote de desenvolvimento do Apache (no Ubuntu, ``apache2-dev``), descompacte o arquivo baixado,
entre no diretório e execute::

  apxs2 -cia mod_xsendfile.c

para compilar, instalar e configurar o módulo.
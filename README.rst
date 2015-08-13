============
Sistema ANSP
============

Sistema de gerenciamento de projetos Fapesp desenvolvido pelo NARA/ANSP.
É um conjunto de aplicações Django para gerenciar concessões e gastos de
um projeto Fapesp.

Instalação
..........

1. Instale os pacotes de desenvolvimento do ``python``, ``xml``, ``ffi``, ``xslt``, ``zlib`` e ``yaml``. No caso do Ubuntu, seria::

    apt-get install libffi-dev libpython-dev libxml2-dev libxslt1-dev zlib1g-dev libyaml-dev

2. Instale o ``virtualenv``::

    pip install virtualenv

3. Crie o ambiente virtual::

    virtualenv <nome do ambiente>

4. Entre no diretório do ambiente virtual e ative-o::

    cd <nome do ambiente>
    source bin/activate

5. Instale o ``django-sistema``::

    pip install --extra-index-url http://10.0.1.65/simple/ django-sistema

Configuração
............

1. Crie um novo projeto Django::

    django-admin startproject <nome do projeto>


2. Adicione a seguinte linha no final seu ``settings.py``::

    INSTALLED_APPS += ('configuracao',)

3. Crie as configurações padrão::

    cd <nome do projeto>
    python manage.py criarsistema <nome do projeto>

4. Execute
   ::

    python manage.py migrate

   para criar a base de dados inicial e
   ::

    python manage.py loaddata initial_data.yaml

   para carregar os dados iniciais.

5. Execute
   ::

    python manage.py createsuperuser

   para criar o super usuário inicial.

6. Execute
   ::

    python manage.py runserver

   e acesse http://localhost:8080 para verificar se a aplicação está rodando.

7. Estando tudo ok nas etapas anteriores, é hora de colocar em produção. Abaixo, é utilizado o Apache + WSGI, mas
pode ser feito de outras maneiras, como descrito em https://docs.djangoproject.com/en/1.7/howto/deployment/ .

    a. Instale o ``apache2``, o ``mod_wsgi``;
    b. Habilite esses módulos;
    c. Configure o apache. Considerando que o sistema rodará sozinho na máquina, a configuração seria apenas
       modificar o arquivo ``/etc/apache2/sites-available/000-default``::

        WSGIScriptAlias / /path/to/your/project/project/wsgi.py
        WSGIPythonPath /path/to/your/project/project:/virtualenv/dir/lib/python2.7/site-packages
        <VirtualHost *:80>

                WSGIProcessGroup %{GLOBAL}
                WSGIApplicationGroup %{GLOBAL}

                Alias /files/   /var/www/files/
                Alias /static/  /var/www/static/

                <Directory /var/www/static>
                   Require all granted
                </Directory>

                <Directory /var/www/files>
                   Require all granted
                </Directory>

                <Directory /path/to/your/project/project>
                   <Files wsgi.py>
                      Require all granted
                   </Files>
                </Directory>

                <Location "/files">
                   AuthType Basic
                   AuthName "Sistema"
                   Require valid-user
                   AuthBasicProvider wsgi
                   WSGIAuthUserScript /path/to/your/project/project/wsgi.py
                </Location>

                ErrorLog ${APACHE_LOG_DIR}/error.log
                CustomLog ${APACHE_LOG_DIR}/access.log combined
        </VirtualHost>

       trocando os diretórios e arquivos informados pelos da sua instalação

    d. Execute, no diretório do projeto::

        python manage.py collectstatic


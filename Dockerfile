
###
# omni
#
# VERSION               git

FROM      debian

MAINTAINER Marco Galicia <galprasmarco@gmail.com>

## update

RUN apt-get update 

##instala apache2 y python

RUN  apt-get install -y python-pip python-yaml python-jinja2 python-paste python-webob python-simplejson openssh-server git apache2  libapache2-mod-wsgi
RUN  apt-get clean
RUN  pip install vincenty geojson webapp2 geopy models



## instala omni

RUN rm /var/www/index.html
RUN cd /var/www/ && git clone https://github.com/zxul767/omnimobi.git

#### configura apache para que aparezca omni

RUN echo " WSGIPythonPath /var/www/omnimobi" > /etc/apache2/sites-enabled/000default
RUN echo " <VirtualHost *:80>" >> /etc/apache2/sites-enabled/000default
RUN echo " DocumentRoot \"/var/www/omnimobi/\"" >> /etc/apache2/sites-enabled/000default
RUN echo " WSGIScriptAlias / \"/var/www/omnimobi/omni.py\"" >> /etc/apache2/sites-enabled/000default
RUN echo " Alias /static/ \"/var/www/omnimobi/static/\"" >> /etc/apache2/sites-enabled/000default
RUN echo " </VirtualHost> " >> /etc/apache2/sites-enabled/000default

### puerto 80


EXPOSE 80


#### empieza apache 

ENV APACHE_RUN_USER www-data
ENV APACHE_RUN_GROUP www-data
ENV APACHE_LOG_DIR /var/log/apache2

CMD a2enmod wsgi
CMD ["/usr/sbin/apache2", "-D", "FOREGROUND"]


### to update image to the lastest realise of omni please use git pull

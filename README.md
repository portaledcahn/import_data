# Portal de Contrataciones Abiertas (Importador de Datos a Elasticsearch)
Librería escrita en Python útil para importar datos de una base de datos OCDS KingFisher en PostgresSQL y pasar a Elasticserach.

## Uso
Las secciones del buscador, visualizaciones y API REST del Portal de Contrataciones Abiertas utilizan como una de sus fuentes de datos el motor de búsqueda Elasticsearch. El importador de datos extrae los registros(records) OCDS de una base de datos de Kingfisher, pre-calcula campos como conversión de monedas, tiempos entre etapas y sumatorias y finalmente almacena documentos en Elasticsearch.

## Requerimientos
* KingFisher (PostgreSQL)
* Python 3.7
* Elasticsearch 6.8

## Instalación paso a paso
A continuación, se explica paso a paso como realizar la instalación del Importador de datos utilizando el sistema operativo Centos 7.

**Paso 1-** Instalar base de datos Kingfisher, ver en: [https://github.com/portaledcahn/edcahn_kingfisher](https://github.com/portaledcahn/edcahn_kingfisher)

**Paso 2-** Instalar Elasticsearch 6.8: 
```
sudo yum install java-1.8.0-openjdk-devel
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-6.8.1.rpm
rpm -ivh elasticsearch-6.8.1.rpm  
sudo systemctl daemon-reload  
sudo systemctl enable elasticsearch.service  
sudo systemctl start elasticsearch.service
vi /etc/elasticsearch/elasticsearch.yml

#Editar/Agregar las siguientes lineas 
cluster.name: edca-elasticseach
network.host: 0.0.0.0
http.port: 9200

sudo systemctl restart elasticsearch.service
netstat -tulpn
curl -X GET "ingresar_aqui_ip_del_servidor:9200/"
```

**Paso 3-** Instalar Python 3.7:
```
sudo yum install gcc openssl-devel bzip2-devel wget libffi-devel xz-devel sqlite-devel postgresql-devel
cd /usr/src
sudo wget https://www.python.org/ftp/python/3.7.3/Python-3.7.3.tgz
sudo tar xzf Python-3.7.3.tgz
cd Python-3.7.3
./configure
./configure --enable-optimizations
make altinstall
vi /root/.bashrc
alias python3='/usr/local/bin/python3.7'
alias pip3='/usr/local/bin/pip3.7'
:wq
```

**Paso 4–** Clonar el repo:
```
mkdir /home/import_to_elastic/
cd /home/import_to_elastic/
git clone https://github.com/portaledcahn/import_data.git
```

**Paso 5–** Instalar virtualenv:
```
pip3 install virtualenv
cd /home/import_to_elastic/
python3 -m venv import_env
source import_env/bin/activate
```

**Paso 6-** Instalar requerimientos:
```
cd /home/import_to_elastic/import_data
pip install -r requirements.txt
```

**Paso 7-** Crear archivo de configuración:
```
cp /home/import_to_elastic/import_data/settings_template.py /home/import_to_elastic/import_data/settings.py
```

**Paso 8-** Editar archivo de configuración, en esta sección es necesario actualizar los parámetros de conexión a las bases de datos kingfisher y Elasticsearch: 
```
vi /home/import_to_elastic/import_data/settings.py

#Credenciales de Elastic
ELASTICSEARCH_SERVER_IP = '127.0.0.1'
ELASTICSEARCH_SERVER_PORT = '9200'
ELASTICSEARCH_USERNAME = 'user'
ELASTICSEARCH_PASS = 'secret'

#Parametros de conexion a kingfisher PostgreSQL
dbHost="127.0.0.1"
dbPort=5432
dbDatabase="ocdskingfisher"
dbUser="postgres"
dbPassword="secret"

:wq
```

**Paso 9-** Crear bash para ejecutar comandos de importación automática:
```
cd /home/import_to_elastic/import_data
cp run_import_template.sh run_import.sh
chmod +x run_import.sh
```

**Paso 10-** Editar archivo bash para establecer las direcciones de las carpetas del importador, entorno virtual y capeta de logs:
```
vi run_import.sh

entorno="/home/import_to_elastic/import_env"
proyecto="/home/import_to_elastic/import_data"
carpeta_logs='/home/import_to_elastic/import_data/logs'

:wq
```

**Paso 11-** Configurar una tarea programada en cron que ejecute el importador de datos automáticamente:
```
crontab -e
* * * * * /home/import_to_elastic/import_data/run_import.sh
:wq
```

## Licencia
Esta obra está bajo una licencia de Creative Commons Reconocimiento 4.0 Internacional.

![CC BY 4.0!](https://i.creativecommons.org/l/by/4.0/88x31.png)

#!/bin/bash

# Extrae los records de postgresql kingfisher e importa a elasticsearch
echo "Iniciando el proceso"
anio_mes=`date +'%Y-%m'`

#Configurar estas carpetas en el proyecto
entorno="/env"
proyecto="/import_data"
carpeta_logs='/import_data/logs'

#Estableciendo el archivo de log
archivo_log="$anio_mes-imports.log"
log="$carpeta_logs/$archivo_log"

#Accediendo a carpeta con el entorno virtual
cd "$entorno"

#Activando el entorno virtual
source bin/activate

#Accediendo a la carpeta del proyecto
cd "$proyecto" 

#Ejecutando importador de kingfisher a elasticsearch
python import_to_elasticserach.py >> "$log" 2>&1

#Actualizar listado de proveedores
python refresh.py >> "$log" 2>&1

echo "Cron Finalizó correctamente"

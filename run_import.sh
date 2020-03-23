#!/bin/bash

# Extraer los records de postgresql kingfisher e importa a elasticsearch

echo "Iniciando el proceso"

#Accediendo a carpeta con el entorno virtual
cd /home/adminaedca/import_elastic/import_env

#Activando el entorno virtual
source bin/activate

#Accediendo a la carpeta del proyecto
cd /home/adminaedca/import_elastic/import_data

#Ejecutando conversor para CE
python import_to_elasticserach.py

echo "Finalizó correctamente"

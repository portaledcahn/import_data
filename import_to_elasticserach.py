import uuid
import os
import elasticsearch.helpers
import time
import ijson
import datetime
import dateutil.parser, dateutil.tz
import simplejson as json
import csv
import sys
import hashlib
import flattentool
import subprocess
import shutil
import codecs
import requests
import pandas
import urllib3
# import psycopg2
from zipfile import ZipFile, ZIP_DEFLATED
from pprint import pprint
import mapeo_es

#Parametros de conexion 
dbHost="192.168.43.163" 
dbPort="5432"
dbDatabaseAdmin="portaledcahn_admin"
dbDatabase="postgres"
dbUser="postgres"
dbPassword="123456"

#Archivos a importar
carpetaArchivos = 'archivos_estaticos/'
pathArchivo = 'archivos_estaticos/pgexport.json'
# pathArchivo = 'archivos_estaticos/pgexport-sefin.json'
# pathArchivo = '/otros/pgexport.json'
pathElastic = 'archivos_estaticos/records.json'

EDCA_INDEX = 'edca'

CONTRACT_INDEX = 'contract' 

TRANSACTION_INDEX = 'transaction'

urllib3.disable_warnings()

"""
    Funcion que se conecta a PostgreSQL (Kingfisher)
    Extrae los records en un archivo .csv 
    Parametro year:
    	Anio a extraer, sera obtenido de compiledRelease.date
"""
def generarRecordCSV(year):
    con = None
    nombreArchivo = "records.csv"
    carpetaArchivos = "archivos_estaticos"

    select = """
		select
			r.ocid,
			d.hash_md5,
			d."data" as "record",
			left(d."data"->'compiledRelease'->>'date',4) as "year"
		from record r
			inner join data d on r.data_id = d.id 
			inner join package_data pd on r.package_data_id = pd.id
		order by
			d.id
		limit 50
    """
    try:
        # raiz = os.path.dirname(os.path.realpath(__file__))
        archivoSalida = os.path.join(carpetaArchivos, nombreArchivo)
        # archivoSalida1 = "{0}\\{1}/{2}".format(raiz, carpetaArchivos, nombreArchivo)
        query = "copy ({0}) To STDOUT With CSV DELIMITER '|';".format(select)

        print(archivoSalida)

        con = psycopg2.connect(
            host=dbHost, 
            port=dbPort,
            database=dbDatabase, 
            user=dbUser, 
            password=dbPassword
        )

        cur = con.cursor()

        with open(archivoSalida, 'w') as f_output:
            cur.copy_expert(query, f_output)

        f_output.close()

    except psycopg2.DatabaseError as e:
        print(f'Error {e}')
        sys.exit(1)

    except IOError as e:
        print(f'Error {e}')
        sys.exit(1)

    finally:
        if con:
            con.close()

def generarRecordHashCSV():
    con = None
    nombreArchivo = "records_hash_year.csv"
    carpetaArchivos = "archivos_estaticos"

    select = """
		select
			r.ocid,
			d.hash_md5,
			left(d."data"->'compiledRelease'->>'date',4) as "year"
		from record r
			inner join data d on r.data_id = d.id 
			inner join package_data pd on r.package_data_id = pd.id
		order by
			d.id
		limit 50
    """
    
    try:
        # raiz = os.path.dirname(os.path.realpath(__file__))
        archivoSalida = os.path.join(carpetaArchivos, nombreArchivo)
        # archivoSalida1 = "{0}\\{1}/{2}".format(raiz, carpetaArchivos, nombreArchivo)
        query = "copy ({0}) To STDOUT With CSV DELIMITER '|';".format(select)

        print(archivoSalida)

        con = psycopg2.connect(
            host=dbHost, 
            port=dbPort,
            database=dbDatabase, 
            user=dbUser, 
            password=dbPassword
        )

        cur = con.cursor()

        with open(archivoSalida, 'w') as f_output:
            cur.copy_expert(query, f_output)

        f_output.close()

    except psycopg2.DatabaseError as e:
        print(f'Error {e}')
        sys.exit(1)

    except IOError as e:
        print(f'Error {e}')
        sys.exit(1)

    finally:
        if con:
            con.close()

def extra_fields_records(ijson, md5):
	separador = ' - '
	extra = {}

	buyerFullName = ijson["compiledRelease"]["buyer"]["name"]
	source = ijson["compiledRelease"]["sources"][0]["id"]

	compiledRelease = ijson["compiledRelease"]

	# Obteniendo padres
	if 'buyer' in compiledRelease:

		if 'name' in compiledRelease["buyer"]:
			buyerFullName = compiledRelease["buyer"]["name"]
		else:
			buyerFullName = 'No proveido'

		if 'id' in compiledRelease['buyer']:
			buyerId = compiledRelease['buyer']['id']

			for p in compiledRelease['parties']:
				if p['id'] == buyerId:
					if 'memberOf' in p:
						parent1 = None
						for m in p['memberOf']:
							parent1 = m
						
						if parent1 is not None: 
							extra['parent1'] = parent1
							buyerFullName = parent1["name"] + ' - ' + buyerFullName
							parentTop = parent1

							for p2 in compiledRelease['parties']:
								if p2['id'] == parent1['id']:
									if 'memberOf' in p2:
										parent2 = None
										for m2 in p2['memberOf']:
											if m2['id'] != parent1['id']:
												parent2 = m2

										if parent2 is not None:
											extra['parent2'] = parent2
											buyerFullName = parent2["name"] + ' - ' + buyerFullName
											parentTop = parent2
					else:
						parentTop = compiledRelease["buyer"]

			buyer = parentTop
		else:
			buyer = None

		extra["buyerFullName"] = buyerFullName
		extra["parentTop"] = parentTop

	# Suma de contratos en tender
	if 'tender' in compiledRelease and 'contracts' in compiledRelease:
		sumContracts = 0
		for c in compiledRelease["contracts"]:
			if 'value' in c: 
				sumContracts += c["value"]["amount"]

		compiledRelease["tender"]["extra"] = {
			"sumContracts": sumContracts
		}

	# Etapa del proceso de contratacion 
	extra["lastSection"] = None

	if 'tender' in compiledRelease:
		extra["lastSection"] = 'tender'

	if 'awards' in compiledRelease:
		extra["lastSection"] = 'awards'

	if 'contracts' in compiledRelease:
		extra["lastSection"] = 'contracts'

	# Precalculo de tiempos
	if 'tender' in compiledRelease:
		if 'tenderPeriod' in compiledRelease['tender']:
			if 'startDate' in compiledRelease['tender']['tenderPeriod']: 
				if 'endDate' in compiledRelease['tender']['tenderPeriod']:
					extra["daysTenderPeriod"] = (dateutil.parser.parse(compiledRelease['tender']['tenderPeriod']['endDate']) - dateutil.parser.parse(compiledRelease['tender']['tenderPeriod']['startDate'])).days
				if 'datePublished' in compiledRelease['tender']:
					extra['daysTenderPublish'] = (dateutil.parser.parse(compiledRelease['tender']['tenderPeriod']['startDate']) - dateutil.parser.parse(compiledRelease['tender']['datePublished'])).days

	extra["hash_md5"] = md5

	return extra

def import_to_elasticsearch(files, clean, forzarInsercion):

	es = elasticsearch.Elasticsearch(max_retries=10, retry_on_timeout=True)

	# Delete the index
	if clean:
		result = es.indices.delete(index=EDCA_INDEX, ignore=[404])
		pprint(result)
		result = es.indices.delete(index=CONTRACT_INDEX, ignore=[404])
		pprint(result)
		result = es.indices.delete(index=TRANSACTION_INDEX, ignore=[404])
		pprint(result)

	result = es.indices.create(index=EDCA_INDEX, body={"mappings": mapeo_es.edca_mapping, "settings": mapeo_es.settings}, ignore=[400])

	if 'error' in result and result['error']['reason'] == 'index EDCA already exists':
		print('Updating existing index')

	result = es.indices.create(index=CONTRACT_INDEX, body={"mappings": mapeo_es.contract_mapping, "settings": mapeo_es.settings}, ignore=[400])

	if 'error' in result and result['error']['reason'] == 'index contract already exists':
		print('Updating existing index')

	result = es.indices.create(index=TRANSACTION_INDEX, body={"mappings": mapeo_es.transaction_mapping, "settings": mapeo_es.settings}, ignore=[400])

	if 'error' in result and result['error']['reason'] == 'index transaction already exists':
		print('Updating existing index')

	time.sleep(1)

	dfTazasCambio = tazasDeCambio()

	def transaction_generator(contract):
		if '_source' in contract:
			if 'implementation' in contract["_source"]:
				if 'transactions' in contract["_source"]["implementation"]:
					for t in contract["_source"]["implementation"]["transactions"]:

						extra = contract["_source"]["extra"]
						extra["contractId"] = contract["_source"]["id"]

						transaction_document = {}
						transaction_document['_id'] = str(uuid.uuid4())
						transaction_document['_index'] = TRANSACTION_INDEX
						transaction_document['_type'] = 'transaction'
						transaction_document['_source'] = t
						transaction_document['_source']['extra'] = extra

						yield transaction_document		

	def contract_generator(compiledRelease):

		extra = {}

		parentTop = {}

		buyerFullName = ''

		if 'ocid' in compiledRelease:
			extra["ocid"] = compiledRelease["ocid"]

		if 'tender' in compiledRelease:
			if 'title' in compiledRelease['tender']:
				extra['tenderTitle'] = compiledRelease["tender"]["title"]

			if 'mainProcurementCategory' in compiledRelease['tender']:
				extra['tenderMainProcurementCategory'] = compiledRelease["tender"]["mainProcurementCategory"]

			if 'additionalProcurementCategories' in compiledRelease['tender']:
				if len(compiledRelease["tender"]["additionalProcurementCategories"]) > 0:
					extra['tenderAdditionalProcurementCategories'] = compiledRelease["tender"]["additionalProcurementCategories"][0]

			if 'procurementMethodDetails' in compiledRelease['tender']:
				extra["tenderProcurementMethodDetails"] = compiledRelease['tender']['procurementMethodDetails']

		#Obteniendo el sistema
		if 'sources' in compiledRelease:
			extra["sources"] = compiledRelease['sources']

		# Obteniendo padres
		if 'buyer' in compiledRelease:

			if 'name' in compiledRelease["buyer"]:
				buyerFullName = compiledRelease["buyer"]["name"]

			if 'id' in compiledRelease['buyer']:
				buyerId = compiledRelease['buyer']['id']

				parentTop = compiledRelease['buyer']

				extra['buyer'] = compiledRelease['buyer']

				for p in compiledRelease['parties']:
					if p['id'] == buyerId:
						if 'memberOf' in p:
							parent1 = None
							for m in p['memberOf']:
								parent1 = m
							
							if parent1 is not None: 
								extra['parent1'] = parent1
								parentTop = parent1
								buyerFullName = parent1["name"] + ' - ' + buyerFullName

								for p2 in compiledRelease['parties']:
									if p2['id'] == parent1['id']:
										if 'memberOf' in p2:
											parent2 = None
											for m2 in p2['memberOf']:
												if m2['id'] != parent1['id']:
													parent2 = m2

											if parent2 is not None:
												extra['parent2'] = parent2
												parentTop = parent2
												buyerFullName = parent2["name"] + ' - ' + buyerFullName

		extra['buyerFullName'] = buyerFullName
		extra['parentTop'] = parentTop

		if 'contracts' in compiledRelease:
			extra["sumTransactions"] = 0
			for c in compiledRelease["contracts"]:
				if 'implementation' in c:
					if 'transactions' in c["implementation"]:
						transactionLastDate = None
						for t in c["implementation"]["transactions"]:
							extra["sumTransactions"] += t["value"]["amount"]

							if transactionLastDate is None: 
								transactionLastDate = t["date"]
							else:
								if t["date"] > transactionLastDate:
									transactionLastDate = t["date"]	

							extra["transactionLastDate"] = transactionLastDate

		extra['fuentes'] = []
		extra['objetosGasto'] = []

		if 'planning' in compiledRelease:
			if 'budget' in compiledRelease['planning']:
				if 'budgetBreakdown' in compiledRelease['planning']['budget']:
					for b in compiledRelease['planning']['budget']['budgetBreakdown']:
						if 'classifications' in b:
							if 'fuente' in b['classifications']:
								extra['fuentes'].append(b['classifications']['fuente'])
								extra['objetosGasto'].append(b['classifications']['objeto'])

		for c in compiledRelease["contracts"]:
			if 'tender' in compiledRelease and 'dateSigned' in c:
				if 'tenderPeriod' in compiledRelease['tender']:
					if 'endDate' in compiledRelease['tender']['tenderPeriod']:
						extra["tiempoContrato"] = (dateutil.parser.parse(c['dateSigned']) - dateutil.parser.parse(compiledRelease['tender']['tenderPeriod']['endDate'])).days

			if 'value' in c:
				if 'amount' in c['value']:

					monedaLocal = {}
					monedaLocal["currency"] = 'HNL'

					if 'dateSigned' in c:
						date = c['dateSigned']
					elif 'period' in c:
						if 'startDate' in c['period']:
							date = c['period']['startDate']
					else:
						date = compiledRelease["date"]

					if 'currency' in c['value']:
						if c['value']['currency'] == 'USD':
							cambio = convertirMoneda(dfTazasCambio, date[0:4], date[5:7], c['value']['amount'])
							
							if cambio is not None:
								monedaLocal["amount"] = c['value']['amount'] * cambio
							else:
								monedaLocal = c['value']['amount']
								monedaLocal["currency"] = c['value']['currency']

						if c['value']['currency'] == 'HNL':
							monedaLocal["amount"] = c['value']['amount']
					else:
						monedaLocal["amount"] = c['value']['amount']
						monedaLocal["currency"] = 'No definido'

					extra['LocalCurrency'] = monedaLocal

			if 'items' in c:
				for i in c['items']:
					i['extra'] = {} 
					if 'unit' in i and 'quantity' in i: 
						if 'value' in i['unit']:
							if 'amount' in i['unit']['value']:
								i['extra']['total'] = float(i['unit']['value']['amount']) * float(i['quantity'])

			contract_document = {}
			contract_document['_id'] = compiledRelease["ocid"] + str(c["id"])
			contract_document['_index'] = CONTRACT_INDEX
			contract_document['_type'] = 'contract'
			contract_document['_source'] = c
			contract_document['_source']['extra'] = extra

			if 'implementation' in c:
				result = elasticsearch.helpers.bulk(es, transaction_generator(contract_document), raise_on_error=False, request_timeout=120)
				print("transaction", result)

			yield contract_document		

	def generador(file_year):
		contador = 0
		numeroColumnaOCID = 0
		numeroColumnaHASH = 1
		numeroColumnaRecord = 2

		for file_name in files:

			file_name = 'archivos_estaticos/records.csv'
			print("Procesando el archivo: ", file_name, file_year)
			# generarRecordCSV(year): # Esta linea es importantisima. 

			csv.field_size_limit(sys.maxsize)
			with open(file_name) as fp:

				reader = csv.reader(fp, delimiter='|')

				for row in reader:
					contador += 1

					record = json.loads(row[numeroColumnaRecord])

					if 'compiledRelease' in record:
						if 'date' in record["compiledRelease"]:
							year = record['compiledRelease']["date"][0:4]

							if year == file_year or forzarInsercion == True:

								exists = recordExists(row[numeroColumnaOCID], row[numeroColumnaHASH])

								if exists != 0 or forzarInsercion == True:
									if exists == 1 or forzarInsercion == True:
										eliminarDocumentoES(row[numeroColumnaOCID])

									document = {}
									document['_id'] = row[numeroColumnaOCID]
									document['_index'] = EDCA_INDEX
									document['_type'] = 'record'
									document['doc'] = record
									document['extra'] = extra_fields_records(record, row[numeroColumnaHASH])

									if 'compiledRelease' in record:
										if 'contracts' in record['compiledRelease']:
											result = elasticsearch.helpers.bulk(es, contract_generator(record['compiledRelease']), raise_on_error=False, request_timeout=120)
											print("contract", result)

									yield document
								else:
									pass
							else:
								pass

			# actualizarArchivoProcesado(year) # Esta linea igual es importantisima.

	years = detectarAniosPorProcesar(files[0])
	# years = ['2017', '2018', '2019']

	print("Por procesar:", years)

	for year in years:
		result = elasticsearch.helpers.bulk(es, generador(year), raise_on_error=False, request_timeout=30)
		print("records procesados", result)

def generate_json_valid(file, outfile):
	cantidad_registros = 0
	contador = 0

	output_file = "archivos_estaticos/" + outfile

	f = open(output_file, "w")
	f.write('[')

	with open(file) as infile:
		for line in infile:
			cantidad_registros += 1

	print('cantidad de registros: ', cantidad_registros)

	with open(file) as infile:
		for line in infile:
			contador += 1
			
			f.write(line)

			if contador != cantidad_registros:
				f.write(',')
			
	f.write(']')
	f.close()

# def generarRecordsPorYear(file, year):
# 	contador = 0
# 	years = ['2017', '2018', '2019']

# 	archivos = [] 

# 	with open(file) as fp:
# 		for record in ijson.items(fp, 'item'):
# 			i_year = ''

# 			file_name = 'todos.json'

# 			if 'compiledRelease' in record:
# 				if 'sources' in record['compiledRelease']:
# 					if len(record['compiledRelease']["sources"]) > 0:
# 							file_name = record['compiledRelease']["sources"][0]["id"]

# 				if 'date' in record['compiledRelease']:
# 					i_year = record['compiledRelease']["date"][0:4]
# 					file_name += "_" + i_year + ".json"

# 			# if i_year in years:		
# 			# 	f = open('archivos_estaticos/records/' + file_name, "a")
# 			# 	f.write(json.dumps(record))
# 			# 	f.write(',')
# 			# 	f.close()

# 			if file_name in archivos:
# 				f = open('archivos_estaticos/records/' + file_name, "a")
# 				f.write(json.dumps(record))
# 				f.write(',')
# 				f.close()
# 			else:
# 				f = open('archivos_estaticos/records/' + file_name, "a")
# 				f.write('[')
# 				f.close()
# 				archivos.append(file_name)

# 			if contador == 20:
# 				break

# 			contador += 1
# 			print('contador', contador)

# 	for a in archivos:
# 		print('Cerrando archivos', a)
# 		f = open('archivos_estaticos/records/' + a, "a")
# 		f.write(']')
# 		f.close()		

# 	print('Contador: ', contador)

def md5(fname):
	hash_md5 = hashlib.md5()

	with open(fname, "rb") as f:
		for chunk in iter(lambda: f.read(4096), b""):
			hash_md5.update(chunk)

	return hash_md5.hexdigest()

def limpiarArchivos(directorio):
	listaArchivos = [ f for f in os.listdir(directorio) if f.endswith(".txt") ]

	for a in listaArchivos:
		open(directorio + a, 'w').close()

def crearDirectorio(directorio):
	try:
		os.stat(directorio)
	except:
		os.mkdir(directorio)

def escribirArchivo(directorio, nombre, texto, modo='a'):
	archivoSalida = codecs.open(directorio + nombre, modo, 'utf-8')
	archivoSalida.write(texto)
	archivoSalida.write('\n')
	archivoSalida.close()

def aplanarArchivo(ubicacionArchivo, directorio):

	flattentool.flatten(
		ubicacionArchivo,
		output_name=directorio,
		main_sheet_name='releases',
		root_list_path='releases',
		root_id='ocid',
		# schema=carpetaArchivos + 'release-schema.json',
		disable_local_refs=True,
		remove_empty_schema_columns=True,
		root_is_list=False
	)

	with ZipFile(directorio + '.zip', 'w', compression=ZIP_DEFLATED) as zipfile:
		for filename in os.listdir(directorio):
			zipfile.write(os.path.join(directorio, filename), filename)
	shutil.rmtree(directorio)

	print('flatten ok')

def generarMetaDatosPaquete(paquetes, md5):

	uri = ''
	license = ''
	version = '1.1'
	publisher = {}
	extensions = []
	publishedDate = ''
	publicationPolicy = ''
	releases = []

	metaDatosPaquete = {}

	fechaActual = datetime.datetime.now(dateutil.tz.tzoffset('UTC', -6*60*60))
	publishedDate = fechaActual.isoformat()

	for p in paquetes:

		paquete = json.loads(p)

		license = paquete['license']
		version = paquete['version']
		publisher = paquete['publisher']
		publicationPolicy = paquete['publicationPolicy']

		for e in paquete['extensions']:
			if not e in extensions:
				extensions.append(e)

	metaDatosPaquete["uri"] = 'http://200.13.162.86/descargas/' + md5 + '.json'
	metaDatosPaquete["version"] = version
	metaDatosPaquete["publishedDate"] = publishedDate
	metaDatosPaquete["publisher"] = publisher
	metaDatosPaquete["extensions"] = extensions
	metaDatosPaquete["license"] = license
	metaDatosPaquete["publicationPolicy"] = publicationPolicy

	return metaDatosPaquete

def generarReleasePackage(paquete, releases, directorio, nombre):
	contador1 = 0
	contador2 = 0
	archivoJson = directorio + nombre

	f = codecs.open(archivoJson, "w", "utf-8")

	#Cargando la data del paquete
	metaDataPaquete = codecs.open(paquete, "r", "utf-8")
	metaData = metaDataPaquete.readlines()
	metaDataPaquete.close()

	for l in metaData[:-1]:
		f.write(l)

	#Creando una estructura para el listado de releases.
	f.write(',"releases": [\n')

	#cargando la data de releases 
	with open(releases) as infile:
		for linea in infile:
			contador1 += 1 

	# Quitando la ultima ,
	with open(releases) as infile:
		for linea in infile:
			if contador2 == contador1 - 1:
				f.write(linea[:-2])
			else:
				f.write(linea)

			contador2 += 1

	#Cerrando el archivo json
	f.write('\n]\n}')

	f.close()

def generarArchivosEstaticos(file):
	contador = 0
	archivos = {}
	archivosProcesar = []
	nombreArchivo = 'salida.csv'
	directorioReleases = carpetaArchivos + 'releases/' 
	directorioHashReleases = directorioReleases + 'hash/'
	directorioTxtReleases = directorioReleases + 'txt/'
	directorioPaquetes = directorioReleases + 'paquetes/'

	numeroColumnaReleaseId = 0
	numeroColumnaOCID = 1
	numeroColumnaHASH = 2
	numeroColumnaPaqueteId = 3
	numeroColumnaRelease = 4
	numeroColumnaPaquete = 5

	crearDirectorio(directorioReleases)
	crearDirectorio(directorioHashReleases)
	crearDirectorio(directorioTxtReleases)
	crearDirectorio(directorioPaquetes)

	limpiarArchivos(directorioHashReleases)
	limpiarArchivos(directorioTxtReleases)
	limpiarArchivos(directorioPaquetes)

	# Generando archivos md5
	csv.field_size_limit(sys.maxsize)
	with open(file) as fp:

		reader = csv.reader(fp, delimiter='|')

		for row in reader:
			llave = ''
			contador += 1

			dataRelease = json.loads(row[numeroColumnaRelease])
			dataPaquete = json.loads(row[numeroColumnaPaquete])

			year = dataRelease["date"][0:4]

			if 'name' in dataPaquete["publisher"]:
				llave = llave + dataPaquete["publisher"]["name"].replace('/', '').replace(' ', '_')[0:17].lower()

			if 'sources' in dataRelease:
				if 'id' in dataRelease["sources"][0]:
					llave = llave + '_' + dataRelease["sources"][0]["id"]

			llave = llave + '_' + year

			if not llave in archivos:
				archivos[llave] = {}
				archivos[llave]["paquetesId"] = []
				archivos[llave]["paquetesData"] = []
				archivos[llave]["archivo_hash"] = directorioHashReleases + llave + '_hash.txt'
				archivos[llave]["archivo_text"] = directorioTxtReleases + llave + '_releases.txt'
				archivos[llave]["archivo_paquete"] = directorioPaquetes + llave + '_paquete.json'

			if not row[numeroColumnaPaqueteId] in archivos[llave]["paquetesId"]:
				archivos[llave]["paquetesId"].append(row[numeroColumnaPaqueteId])
				archivos[llave]["paquetesData"].append(row[numeroColumnaPaquete])

			escribirArchivo(directorioHashReleases, llave + '_hash.txt', row[numeroColumnaHASH])
			escribirArchivo(directorioTxtReleases, llave + '_releases.txt', row[numeroColumnaRelease] + ',')

		print('ya: contador->', contador)

		for llave in archivos:
			archivo = archivos[llave]
			archivo["md5_hash"] = md5(archivo["archivo_hash"])
			archivosProcesar.append(llave)
			# print(archivos[year])

		#Comparar archivos MD5

		#Generar release package
		for llave in archivos:
			if llave in archivosProcesar:
				metaDataPaquete = generarMetaDatosPaquete(archivos[llave]['paquetesData'], archivos[llave]['md5_hash'])
				escribirArchivo(directorioPaquetes, llave + '_paquete.json', json.dumps(metaDataPaquete, indent=4, ensure_ascii=False), 'w')
				generarReleasePackage(archivos[llave]["archivo_paquete"], archivos[llave]["archivo_text"], directorioReleases, llave + '.json')
				archivos[llave]["json"] = directorioReleases + llave + '.json'
				archivos[llave]["md5"] = md5(archivos[llave]["json"])
				escribirArchivo(directorioReleases, llave + '.md5', archivos[llave]["md5"], 'w')

		escribirArchivo(carpetaArchivos, 'archivos.json', json.dumps(archivos, ensure_ascii=False), 'w')

		for llave in archivos:
			if llave in archivosProcesar:
				aplanarArchivo(archivos[llave]['json'], directorioReleases + llave)
				archivos[llave]["excel"] = directorioReleases + llave + '.xlsx'
				archivos[llave]["csv"] = directorioReleases + llave + '.zip'


		# for row in reader:
		# 	data = json.loads(row[numeroColumnaRelease])
		# 	year = data["date"][0:4]

		# 	if year in archivosProcesar:
				
	# for a in archivos:
	# 	f = open('archivos_estaticos/releases/' + a, "a")
	# 	f.write(']')
	# 	f.close()		

"""
	Consulta en el indice de elasticsearch por ocid y hash_md5 si el record existe y si cambio. 
	Retorna: 
		0 = El record existe y no ha cambiado
		1 = El record existe y cambio
		2 = El record no existe. 
"""
def recordExists(ocid, md5):
	campos = ['extra.hash_md5']

	try:
		es = elasticsearch.Elasticsearch(max_retries=10, retry_on_timeout=True)
		res = es.get(index="edca", doc_type='record', id=ocid, _source=campos)

		esMD5 = res['_source']['extra']['hash_md5']

		if esMD5 == md5:
			respuesta = 0 # El record existe y no ha cambiado
		else:
			respuesta = 1 # El record existe y cambio

	except Exception as e:
		respuesta = 2 # El record no existe. 

	return respuesta

"""
	Elimina los documentos indexados en elasticsearch asociados a un OCID 
"""
def eliminarDocumentoES(ocid):

	query = {'query': {'term':{'extra.ocid.keyword':ocid}}}

	try:
		es = elasticsearch.Elasticsearch(max_retries=10, retry_on_timeout=True)

		if es.indices.exists(index="contract"):
			res = es.delete_by_query(
				index="contract",
				body=query
			)

		query = {'query': {'term':{'extra.ocid.keyword':ocid}}}

		if es.indices.exists(index="transaction"):
			res = es.delete_by_query(
				index="transaction",
				body=query
			)
	except Exception as e:
		print(e) 

"""
	Parametro de entrada un .csv separado por el delimitador | ej. ocid | hash_md5 | data.json | anio
	Retorna un listado de los años que han tenido cambios.
"""
def detectarAniosPorProcesar(archivo):
	archivos = {}
	aniosPorProcesar = []
	contador = 0
	numeroColumnaOCID = 0
	numeroColumnaHASH = 1
	numeroColumnaYear = 2
	directorioRecordsHash = carpetaArchivos + 'records_hash/'

	crearDirectorio(directorioRecordsHash)
	limpiarArchivos(directorioRecordsHash)

	# Generando archivos md5
	csv.field_size_limit(sys.maxsize)
	with open(archivo) as fp:

		reader = csv.reader(fp, delimiter='|')

		for row in reader:
			llave = ''
			contador += 1

			llave = row[numeroColumnaYear]

			if not llave in archivos:
				archivos[llave] = {}
				archivos[llave]["year"] = llave
				archivos[llave]["archivo_hash"] = directorioRecordsHash + llave + '_hash.txt'

			escribirArchivo(directorioRecordsHash, llave + '_hash.txt', row[numeroColumnaHASH])

	for llave in archivos:
		archivoHash = archivos[llave]
		archivoHash["md5_hash"] = md5(archivoHash["archivo_hash"])

	#Comparar archivos MD5
	archivoJson = directorioRecordsHash + 'year.json'

	try:
		with open(archivoJson) as json_file:
			years = json.load(json_file)
	except Exception as e:
		years = {}

	for a in archivos:
		year = archivos[a]

		if a in years:
			if year["md5_hash"] != years[a]["md5_hash"]:
				aniosPorProcesar.append(a)
		else:
			aniosPorProcesar.append(a)

	#Guardar el archivo .json con los hash
	escribirArchivo(directorioRecordsHash, 'year.json', json.dumps(archivos, ensure_ascii=False), 'w')

	return aniosPorProcesar

"""
	Genera o actualiza el archivo tazas_de_cambio.csv utilizado para convertir monedas USD a HNL.
	ver https://www.bch.hn/tipo_de_cambiom.php
	retorna un pandas.dataframe donde las filas son meses y las columnas son anios.
"""
def tazasDeCambio():
	archivo = carpetaArchivos + 'tazas_de_cambio.xls'
	archivoCSV = carpetaArchivos + 'tazas_de_cambio.csv'
	serieMensualUSD = 'https://www.bch.hn/esteco/ianalisis/proint.xls'

	try:
		obtenerArchivoExcel = requests.get(serieMensualUSD, verify=False)
		open(archivo, 'wb').write(obtenerArchivoExcel.content)
		tc = pandas.read_excel(io=archivo, sheet_name='proint', header=16, index_col=None, nrows=13)
		tc = tc.drop(columns=['Unnamed: 0'], axis=1)
	except Exception as e:
		tc = pandas.DataFrame([])

	if not tc.empty:
		tc.to_csv(path_or_buf=archivoCSV, index=False)
	else:
		tc = pandas.read_csv(filepath_or_buffer=archivoCSV) 

	return tc

def convertirMoneda(dfTazasDeCambio, anio, mes, monto):
	montoHNL = None

	try:
		monthRow = int(mes) - 1 #promedio del mes, en las filas comienza enero es 0, febrero es 1 por eso se resta 1.
		yearColumn = int(anio)
	except Exception as e:
		now = datetime.datetime.now()
		monthRow = 12 #Promedio anual
		yearColumn = now.year #promedio del anio acual.

	try:
		tazaDecambio = dfTazasDeCambio.loc[monthRow, yearColumn]
	except Exception as e:
		tazaDecambio = None

	if tazaDecambio is not None:
		montoHNL = tazaDecambio * monto

	return montoHNL

def pruebas(files):
	print('probando')
	contador = 0
	years = ['2017', '2018', '2019']

	numeroColumnaOCID = 0
	numeroColumnaHASH = 1
	numeroColumnaRecord = 2

	tc = tazasDeCambio()

	# eliminarDocumentoES('ocds-lcuori-7GXa9R-CMA-UDH-142-2018-1')
	# recordExists('ocds-lcuori-MLQmwL-CM-047-2018-1', '1')

	for file_name in files:

		csv.field_size_limit(sys.maxsize)
		with open(file_name) as fp:

			reader = csv.reader(fp, delimiter='|')

			for row in reader:
				contador += 1

				record = json.loads(row[numeroColumnaRecord])

				if 'compiledRelease' in record:
				# 	print("Si compiledRelease")
					if 'date' in record["compiledRelease"]:
						year = record['compiledRelease']["date"][0:4]
						month = record['compiledRelease']["date"][5:7]

						try:
							monthRow = int(month) - 1 #promedio del mes, en las filas comienza enero es 0, febrero es 1 por eso se resta 1.
							yearColumn = int(year)
						except Exception as e:
							now = datetime.datetime.now()
							monthRow = 12 #Promedio anual
							yearColumn = now.year #promedio del año acual.

						if 'contracts' in record["compiledRelease"]:
							for c in record["compiledRelease"]["contracts"]:
								if 'value' in c:
									if 'amount' in c['value']:
										cambio = tc.loc[monthRow, yearColumn] * c['value']['amount']
										
										print("year", year)
										print("month", month, 'int:month', int(month))
										print("date", record['compiledRelease']["date"])
										print("monto del contrato:", c['value']['amount'])
										print("tc", convertirMoneda(tc, year, month, c['value']['amount']))
										print("valor HNL", cambio)

						if contador > 5:
							exit(0)

				# 		print("ok date")
				# 		if year:
				# 			print("ok year")
				# 			document = {}
				# 			document['_id'] = str(uuid.uuid4())
				# 			document['_index'] = EDCA_INDEX
				# 			document['_type'] = 'record'
				# 			document['doc'] = record
				# 			document['extra'] = extra_fields(record)

				# 			print("ok documento", contador)

				# 			# yield document
				# 		else:
				# 			pass
				# 	else:
				# 		print("No date")
				# else:
				# 	print("No compiledRelease")

def main():
	# Tener en cuenta se necesita crear el archivo de recods.csv primero
	startDate = datetime.datetime.now()
	print("Fecha de inicio:  ", startDate)

	#Ejecutar comandos aqui
	# generarRelasesCSV() # Importantisimo esta linea.
	archivoRecordsHash = 'archivos_estaticos/records_hash_year.csv'
	archivoRecords = 'archivos_estaticos/records.csv'
	import_to_elasticsearch([archivoRecordsHash,], False, False)
	# pruebas([archivoRecords,])
	# print(detectarAniosPorProcesar(archivoRecordsHash))

	endDate = datetime.datetime.now()
	elapsedTime = endDate-startDate
	minutes = (elapsedTime.seconds) / 60

	print("Fecha y hora fin: ", endDate)
	print("Tiempo transcurrido: " + str(minutes) + " minutos")

#Ejecutando el programa.
main()


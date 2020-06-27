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
import psycopg2
import copy
from dateutil.relativedelta import relativedelta
from zipfile import ZipFile, ZIP_DEFLATED
from pprint import pprint
import mapeo_es, settings

#Archivos a importar
carpetaArchivos = 'archivos_estaticos/'

#Parametros de conexion a kingfisher PostgreSQL
dbHost=settings.dbHost
dbPort=settings.dbPort
dbDatabase=settings.dbDatabase
dbUser=settings.dbUser
dbPassword=settings.dbPassword

#Parametros de conexion a Elasticsearch
ES_IP = settings.ELASTICSEARCH_SERVER_IP
ES_PORT = settings.ELASTICSEARCH_SERVER_PORT
ELASTICSEARCH_DSL_HOST = '{0}:{1}/'.format(ES_IP, ES_PORT)
ELASTICSEARCH_USERNAME = settings.ELASTICSEARCH_USERNAME
ELASTICSEARCH_PASS = settings.ELASTICSEARCH_PASS

EDCA_INDEX = 'edca'
CONTRACT_INDEX = 'contract' 
TRANSACTION_INDEX = 'transaction'

urllib3.disable_warnings()

"""
	Funcion que se conecta a PostgreSQL (Kingfisher)
"""
def generarRecordHashCSV():
	con = None
	nombreArchivo = "records_hash_year.csv"
	carpetaArchivos = "archivos_estaticos"

	# where = """ where r.ocid in (
	# 	'ocds-lcuori-jRD4QR-LP-11-2005-2'
	# ) """

	# where = """ where left(d."data"->'compiledRelease'->>'date',4) in ('2019', '2020') """

	where = ""

	select = """
		select
			r.ocid,
			d.hash_md5,
			left(d."data"->'compiledRelease'->>'date',4) as "year"
		from record r
			inner join data d on r.data_id = d.id 
			inner join package_data pd on r.package_data_id = pd.id
		{0}
		order by
			r.id
		--limit 5
	""".format(where)

	try:
		archivoSalida = os.path.join(carpetaArchivos, nombreArchivo)
		query = "copy ({0}) To STDOUT With CSV DELIMITER '|';".format(select)

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

	# where = """ and not d."data"->'compiledRelease'->'sources' @> '[{"id":"HN.SIAFI2"}]' """
	# where = """ and r.ocid in (
	# 	'ocds-lcuori-jRD4QR-LP-11-2005-2'
	# ) """

	where = ""

	select = """
		select
			r.ocid,
			d.hash_md5,
			d."data" as "record",
			left(d."data"->'compiledRelease'->>'date',4) as "year"
		from record r
			inner join data d on r.data_id = d.id 
			inner join package_data pd on r.package_data_id = pd.id
		where 
			left(d."data"->'compiledRelease'->>'date',4) = '{0}' {1}
		order by
			d.id
		--limit 5
	""".format(year, where)

	try:
		archivoSalida = os.path.join(carpetaArchivos, nombreArchivo)
		query = "copy ({0}) To STDOUT With CSV DELIMITER '|';".format(select)

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

"""
	Agrega campos adicionales al record, precalculos de timepos y conversion de montos.
"""
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

"""
	Realiza el ETL de Kingfisher a Elasticsearch
	forzarInsercionYear = True, vuelve a procesar un anio aunque el hash de records sea el mismo. 
	forzarInsercionRecords = True, vuelve a procesar cada record aunque ya este indexando en elasticsearch y el hash sea el mismo.
"""
def import_to_elasticsearch(files, forzarInsercionYear, forzarInsercionRecords):
	print("importando a ES")

	es = elasticsearch.Elasticsearch(ELASTICSEARCH_DSL_HOST, timeout=120, http_auth=(ELASTICSEARCH_USERNAME, ELASTICSEARCH_PASS))

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

			if 'tenderPeriod' in compiledRelease['tender']:
				if 'startDate' in compiledRelease['tender']['tenderPeriod']:
					extra["tenderPeriodStartDate"] = compiledRelease['tender']['tenderPeriod']['startDate']

				if 'endDate' in compiledRelease['tender']['tenderPeriod']:
					extra["tenderPeriodEndDate"] = compiledRelease['tender']['tenderPeriod']['endDate']


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
		extra['fuentesONCAE'] = []

		# planning/budget/budgetBreakdown/0/sourceParty/name

		if 'planning' in compiledRelease:
			if 'budget' in compiledRelease['planning']:
				if 'budgetBreakdown' in compiledRelease['planning']['budget']:
					for b in compiledRelease['planning']['budget']['budgetBreakdown']:
						if 'classifications' in b:
							if 'fuente' in b['classifications']:
								extra['fuentes'].append(b['classifications']['fuente'])
								extra['objetosGasto'].append(b['classifications']['objeto'])

						if 'sourceParty' in b:
							if 'name' in b['sourceParty']:
								extra['fuentesONCAE'].append(b['sourceParty']['name'])

		for c in compiledRelease["contracts"]:
			if 'tender' in compiledRelease and 'dateSigned' in c:
				if 'tenderPeriod' in compiledRelease['tender']:
					if 'endDate' in compiledRelease['tender']['tenderPeriod']:
						extra["tiempoContrato"] = ((dateutil.parser.parse(c['dateSigned'])).date() - (dateutil.parser.parse(compiledRelease['tender']['tenderPeriod']['endDate'])).date()).days

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
								monedaLocal["exchangeRate"] = cambio
							else:
								monedaLocal["amount"] = c['value']['amount']
								monedaLocal["currency"] = c['value']['currency']
								monedaLocal["exchangeRate"] = 1

						if c['value']['currency'] == 'HNL':
							monedaLocal["amount"] = c['value']['amount']
							monedaLocal["exchangeRate"] = 1
					else:
						monedaLocal["amount"] = c['value']['amount']
						monedaLocal["exchangeRate"] = 1

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
				# print("transaction", result)

			yield contract_document		

	def generador(file_year):
		contador = 0
		numeroColumnaOCID = 0
		numeroColumnaHASH = 1
		numeroColumnaRecord = 2

		for file_name in files:

			file_name = 'archivos_estaticos/records.csv'
			print("Procesando el archivo: ", file_name, file_year)
			generarRecordCSV(file_year)

			csv.field_size_limit(sys.maxsize)
			with open(file_name) as fp:

				reader = csv.reader(fp, delimiter='|')

				for row in reader:
					contador += 1

					record = json.loads(row[numeroColumnaRecord])

					if 'compiledRelease' in record:
						if 'date' in record["compiledRelease"]:
							year = record['compiledRelease']["date"][0:4]

							if year == file_year or forzarInsercionYear == True:

								exists = recordExists(row[numeroColumnaOCID], row[numeroColumnaHASH])

								# print(row[numeroColumnaOCID], ',', exists)

								if exists != 0 or forzarInsercionRecords == True:
									if exists == 1 or forzarInsercionRecords == True:
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
											# print("contract", result)

									yield document
								else:
									pass
							else:
								pass

			actualizarArchivoProcesado(file_year, contador) #Indicando que el archivo se proceso completo.

	#Linea importante para procesar solo lo necesario
	years = detectarAniosPorProcesar(files[0])
	# years = ['2018',] # Variable para forzar la insercion de un anio especifico

	print("Por procesar:", years)

	for year in years:
		result = elasticsearch.helpers.bulk(es, generador(year), raise_on_error=False, request_timeout=30)
		print("records procesados", result)

"""
	Genera el hash md5 de un archivo de texto
"""
def md5(fname):
	hash_md5 = hashlib.md5()

	with open(fname, "rb") as f:
		for chunk in iter(lambda: f.read(4096), b""):
			hash_md5.update(chunk)

	return hash_md5.hexdigest()

"""
	Elimina el contenido de un archivo de texto
"""
def limpiarArchivos(directorio):
	listaArchivos = [ f for f in os.listdir(directorio) if f.endswith(".txt") ]

	for a in listaArchivos:
		open(directorio + a, 'w').close()

"""
	Crear un directorio, solo si no existe
"""
def crearDirectorio(directorio):
	try:
		os.stat(directorio)
	except:
		os.mkdir(directorio)

"""
	Escribe en un archivo de texto/
"""
def escribirArchivo(directorio, nombre, texto, modo='a'):
	archivoSalida = codecs.open(directorio + nombre, modo, 'utf-8')
	archivoSalida.write(texto)
	archivoSalida.write('\n')
	archivoSalida.close()

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
		es = elasticsearch.Elasticsearch(ELASTICSEARCH_DSL_HOST, max_retries=10, retry_on_timeout=True, http_auth=(ELASTICSEARCH_USERNAME, ELASTICSEARCH_PASS))
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
		es = elasticsearch.Elasticsearch(ELASTICSEARCH_DSL_HOST, max_retries=10, retry_on_timeout=True, http_auth=(ELASTICSEARCH_USERNAME, ELASTICSEARCH_PASS))

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
		archivoHash["finalizo"] = False
		archivoHash["nroRecords"] = 0

	#Comparar archivos MD5, archivoJson contiene los datos que han sido procesados.
	archivoJson = directorioRecordsHash + 'year.json'

	try:
		with open(archivoJson) as json_file:
			years = json.load(json_file)
	except Exception as e:
		years = {}

	for a in archivos:
		year = archivos[a]

		if a in years: #years contiene los archivos que ya fueron procesados.
			year["finalizo"] = years[a]["finalizo"]
			year["nroRecords"] = years[a]["nroRecords"]

			# Si los hash son diferentes entonces se procesa.
			if year["md5_hash"] != years[a]["md5_hash"]:
				years[a]["md5_hash"] = year["md5_hash"] #Se actualiza el valor del hash
				aniosPorProcesar.append(a)
			else:
				# Si no se termino de procesar completo, entonces se procesa de nuevo.
				if years[a]['finalizo'] == False:
					aniosPorProcesar.append(a)
				else:
					year = copy.deepcopy(years[a])
		else:
			# Si el anio nunca habia sido procesado, entonces se procesa. 
			aniosPorProcesar.append(a)
			# Tambien se agrega al archivo para seguimiento.
			years[a] = copy.deepcopy(year)

	#Guardar el archivo .json con los hash
	escribirArchivo(directorioRecordsHash, 'year.json', json.dumps(years, ensure_ascii=False), 'w')

	return aniosPorProcesar

"""
	Establece como true en el archivo .json de hash_md5 cuando el proceso finalizo por completo
	Tambien indica la cantidad de records procesados.
"""
def actualizarArchivoProcesado(year, contador):
	archivos = {}
	directorioRecordsHash = carpetaArchivos + 'records_hash/'
	archivoJson = directorioRecordsHash + 'year.json'

	try:
		with open(archivoJson) as json_file:
			files_hash = json.load(json_file)

			if year in files_hash:
				files_hash[year]["finalizo"] = True
				files_hash[year]["nroRecords"] = contador

			escribirArchivo(directorioRecordsHash, 'year.json', json.dumps(files_hash, ensure_ascii=False), 'w')

	except Exception as e:
		print("Error", str(e))


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
		print("error", e)
		tc = pandas.DataFrame([])

	if not tc.empty:
		tc.to_csv(path_or_buf=archivoCSV, index=False)
	else:
		tc = pandas.read_csv(filepath_or_buffer=archivoCSV) 

	return tc

"""
	Conversor de montos de USD a HNL.
"""
def convertirMoneda(dfTazasDeCambio, anio, mes, monto):
	tc = None

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
		tc = tazaDecambio

	return tc

"""
	Funcion para realizar pruebas, puede ser eliminada en cualquier momento.
"""
def pruebas(files):
	print('probando')
	contador = 0
	years = ['2017', '2018', '2019']

	# generarRecordCSV('2018')

	# tz = tazasDeCambio()

	# print(tz.head())
	# print(tz[['MES',2018]])

	# generarRecordHashCSV()
	# years = detectarAniosPorProcesar('archivos_estaticos/records_hash_year.csv')
	# print(years)
	# archivoRecordsHash = 'archivos_estaticos/records_hash_year.csv'
	# import_to_elasticsearch([archivoRecordsHash,], False, False, False)

	# numeroColumnaOCID = 0
	# numeroColumnaHASH = 1
	# numeroColumnaRecord = 2

	# tc = tazasDeCambio()

	# eliminarDocumentoES('ocds-lcuori-7GXa9R-CMA-UDH-142-2018-1')
	# recordExists('ocds-lcuori-MLQmwL-CM-047-2018-1', '1')

	# for file_name in files:

	# 	csv.field_size_limit(sys.maxsize)
	# 	with open(file_name) as fp:

	# 		reader = csv.reader(fp, delimiter='|')

	# 		for row in reader:
	# 			contador += 1

	# 		print("Registros", contador)
				# record = json.loads(row[numeroColumnaRecord])

				# if contador == 206001:
					# print("OCID 206001", row[numeroColumnaOCID])
					# exit(0)
				# if 'compiledRelease' in record:
				# # 	print("Si compiledRelease")
				# 	if 'date' in record["compiledRelease"]:
				# 		year = record['compiledRelease']["date"][0:4]
				# 		month = record['compiledRelease']["date"][5:7]

				# 		try:
				# 			monthRow = int(month) - 1 #promedio del mes, en las filas comienza enero es 0, febrero es 1 por eso se resta 1.
				# 			yearColumn = int(year)
				# 		except Exception as e:
				# 			now = datetime.datetime.now()
				# 			monthRow = 12 #Promedio anual
				# 			yearColumn = now.year #promedio del año acual.

				# 		if 'contracts' in record["compiledRelease"]:
				# 			for c in record["compiledRelease"]["contracts"]:
				# 				if 'value' in c:
				# 					if 'amount' in c['value']:
				# 						cambio = tc.loc[monthRow, yearColumn] * c['value']['amount']
										
				# 						print("year", year)
				# 						print("month", month, 'int:month', int(month))
				# 						print("date", record['compiledRelease']["date"])
				# 						print("monto del contrato:", c['value']['amount'])
				# 						print("tc", convertirMoneda(tc, year, month, c['value']['amount']))
				# 						print("valor HNL", cambio)

				# 		if contador > 5:
				# 			exit(0)

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

"""
	Funcion principal, ejecuta las funciones para el proceso de importacion de PostgresSQL (PG) a ElasticSearch(ES).
"""
def main():
	# Tener en cuenta se necesita crear el archivo de recods.csv primero
	startDate = datetime.datetime.now()
	print("\nFecha de inicio:  ", startDate)

	#Ejecutar comandos aqui
	generarRecordHashCSV() # Gerando archivo hash de records hashs.
	archivoRecordsHash = 'archivos_estaticos/records_hash_year.csv'
	import_to_elasticsearch([archivoRecordsHash,], False, False)
	
	# archivoRecords = 'archivos_estaticos/records.csv'
	# pruebas([archivoRecords,])

	endDate = datetime.datetime.now()
	elapsedTime = endDate-startDate
	minutes = (elapsedTime.seconds) / 60

	print("Fecha y hora fin: ", endDate)
	print("Tiempo transcurrido: " + str(minutes) + " minutos")

#Ejecutando el programa.
main()


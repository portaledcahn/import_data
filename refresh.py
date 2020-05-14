from elasticsearch import Elasticsearch, helpers
from elasticsearch_dsl import Search, Q, A
import string, random, copy, datetime
import mapeo_es, settings

ELASTICSEARCH_DSL_HOST = '{0}:{1}/'.format(settings.ELASTICSEARCH_SERVER_IP, settings.ELASTICSEARCH_SERVER_PORT) #No agregar en esta línea.
ELASTICSEARCH_USERNAME = settings.ELASTICSEARCH_USERNAME
ELASTICSEARCH_PASS = settings.ELASTICSEARCH_PASS

""" Funcion para pre-cargar los datos de proveedores. """
def cadenaAleatoria(stringLength=8):
	letters = string.ascii_lowercase
	return ''.join(random.choice(letters) for i in range(stringLength))

def eliminarProveedoresES(procesoId):
	query = {"query":{"bool":{"must_not":[{"term":{"procesoImportacionId.keyword":"{0}".format(procesoId)}}]}}}

	try:
		es = Elasticsearch(
			ELASTICSEARCH_DSL_HOST, 
			timeout=120, 
			http_auth=(ELASTICSEARCH_USERNAME, ELASTICSEARCH_PASS)
		)

		if es.indices.exists(index="supplier"):
			res = es.delete_by_query(index="supplier",body=query)

	except Exception as e:
		print("Advertencia al eliminar")

def scanAggs(search, source_aggs, inner_aggs={}, size=10):
    """
    Helper function used to iterate over all possible bucket combinations of
    ``source_aggs``, returning results of ``inner_aggs`` for each. Uses the
    ``composite`` aggregation under the hood to perform this.
    """
    def run_search(**kwargs):
        s = search[:0]
        s.aggs.bucket('comp', 'composite', sources=source_aggs, size=size, **kwargs)
        for agg_name, agg in inner_aggs.items():
            s.aggs['comp'][agg_name] = agg
        return s.execute()

    response = run_search()
    while response.aggregations.comp.buckets:
        for b in response.aggregations.comp.buckets:
            yield b
        if 'after_key' in response.aggregations.comp:
            after = response.aggregations.comp.after_key
        else:
            after= response.aggregations.comp.buckets[-1].key
        response = run_search(after=after)

def importarProveedores():
	cliente = Elasticsearch(
		ELASTICSEARCH_DSL_HOST, 
		timeout=120, 
		http_auth=(ELASTICSEARCH_USERNAME, ELASTICSEARCH_PASS)
	)

	s = Search(using=cliente, index='transaction')

	proveedores = A('terms', field='payee.id.keyword')

	nombre = A('terms', field='payee.name.keyword')
	totalMontoContratado = A('sum', field='value.amount')
	promedioMontoContratado = A('avg', field='value.amount')
	mayorMontoContratado = A('max', field='value.amount')
	menorMontoContratado = A('min', field='value.amount')
	fechaUltimoProceso = A('max', field='date')
	procesos = A('cardinality', field='extra.ocid.keyword')

	proveedorAgg = {'id': proveedores}

	calculosAgg = {
		'name': nombre,
		'total_monto_contratado': totalMontoContratado, 
		'promedio_monto_contratado': promedioMontoContratado,
		'mayor_monto_contratado': mayorMontoContratado,
		'menor_monto_contratado': menorMontoContratado,
		'fecha_ultimo_proceso': fechaUltimoProceso,
		'procesos': procesos
	}

	procesoImportacionId = cadenaAleatoria(10)
	print("Proces de importación: ", procesoImportacionId)

	result = cliente.indices.create(index="supplier", body={"mappings": mapeo_es.supplier_mapping, "settings": mapeo_es.settings}, ignore=[400])

	if 'error' in result and result['error']['reason'] == 'index supplier already exists':
		print('Updating existing index')
	else:
		print(result)

	def importar_datos(idProceso):
		for p in scanAggs(s, proveedorAgg, calculosAgg,  size=2):

			if len(p["name"]["buckets"]) > 0:
				nombre = p["name"]["buckets"][0]["key"]
			else:
				nombre = ''

			document = {}
			document['_id'] = 'SIAFI-' + p["key"]["id"] + nombre
			document['_index'] = 'supplier'
			document['_type'] = 'supplier'
			document['id'] = p["key"]["id"]
			document['name'] = nombre
			document['procesos'] = p["procesos"]["value"]
			document['total_monto_pagado'] = p["total_monto_contratado"]["value"]
			document['promedio_monto_pagado'] = p["promedio_monto_contratado"]["value"]
			document['mayor_monto_pagado'] = p["mayor_monto_contratado"]["value"]
			document['menor_monto_pagado'] = p["menor_monto_contratado"]["value"]
			document['fecha_ultimo_proceso'] = p["fecha_ultimo_proceso"]["value_as_string"]
			document['publicador'] = "SEFIN"
			document["procesoImportacionId"] = idProceso

			yield document

	result = helpers.bulk(cliente, importar_datos(procesoImportacionId), raise_on_error=False, request_timeout=120)

	eliminarProveedoresES(procesoImportacionId)

if __name__ == '__main__':

	startDate = datetime.datetime.now()
	print("Fecha de inicio:  ", startDate)

	importarProveedores()

	endDate = datetime.datetime.now()
	elapsedTime = endDate-startDate
	minutes = (elapsedTime.seconds) / 60

	print("Fecha y hora fin: ", endDate)
	print("Tiempo transcurrido: " + str(minutes) + " minutos")

	print("Refresh proveedores ok.")

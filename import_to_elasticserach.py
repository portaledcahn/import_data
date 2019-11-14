# import json
# import argparse
# import flattentool
# import shutil
import uuid
# import tempfile
import os
# import csv
# import gzip
from pprint import pprint
import elasticsearch.helpers
# import requests
import time
import ijson
import datetime
import dateutil.parser, dateutil.tz
import simplejson as json

#Archivos a importar
pathArchivo = 'archivos_estaticos/pgexport.json'
# pathArchivo = 'archivos_estaticos/pgexport-sefin.json'
# pathArchivo = '/otros/pgexport.json'
pathElastic = 'archivos_estaticos/records.json'

ES_INDEX = os.environ.get("ES_INDEX", "edca")

CONTRACT_INDEX = 'contract' 

TRANSACTION_INDEX = 'transaction'

def contract_to_elastic(contract):
	pass

def extra_fields(ijson):
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

	return extra

def import_to_elasticsearch(files, clean):

	es = elasticsearch.Elasticsearch(max_retries=10, retry_on_timeout=True)
	# es = elasticsearch.Elasticsearch('http://200.13.162.87:9200/')

	# Delete the index
	if clean:
		result = es.indices.delete(index=ES_INDEX, ignore=[404])
		pprint(result)
		result = es.indices.delete(index=CONTRACT_INDEX, ignore=[404])
		pprint(result)
		result = es.indices.delete(index=TRANSACTION_INDEX, ignore=[404])
		pprint(result)

	mappings = {
	  "record" : {
	    "properties" : {
	      "doc" : {
	        "properties" : {
	          "compiledRelease" : {
	            "properties" : {
	              "awards" : {
	                "properties" : {
	                  "description" : {
	                    "type" : "text",
	                    "fields" : {
	                      "keyword" : {
	                        "type" : "keyword",
	                        "ignore_above" : 256
	                      }
	                    }
	                  },
	                  "documents" : {
	                    "properties" : {
	                      "datePublished" : {
	                        "type" : "date"
	                      },
	                      "description" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "documentType" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "id" : {
	                        "type" : "long"
	                      },
	                      "title" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "url" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "id" : {
	                    "type" : "text"
	                  },
	                  "items" : {
	                    "properties" : {
	                      "classification" : {
	                        "properties" : {
	                          "description" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "id" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "scheme" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          }
	                        }
	                      },
	                      "description" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "id" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "quantity" : {
	                        "type" : "float"
	                      },
	                      "unit" : {
	                        "properties" : {
	                          "name" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "properties" : {
	                              "amount" : {
	                                "type" : "float"
	                              }
	                            }
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "suppliers" : {
	                    "properties" : {
	                      "id" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "name" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "title" : {
	                    "type" : "text",
	                    "fields" : {
	                      "keyword" : {
	                        "type" : "keyword",
	                        "ignore_above" : 256
	                      }
	                    }
	                  },
	                  "value" : {
	                    "properties" : {
	                      "amount" : {
	                        "type" : "float"
	                      },
	                      "currency" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      }
	                    }
	                  }
	                }
	              },
	              "buyer" : {
	                "properties" : {
	                  "id" : {
	                    "type" : "text",
	                    "fields" : {
	                      "keyword" : {
	                        "type" : "keyword",
	                        "ignore_above" : 256
	                      }
	                    }
	                  },
		              "name" : {
						"type" : "text",
						"analyzer": "ngram_analyzer",
						"search_analyzer": "whitespace_analyzer",
						"fields" : {
							"keyword" : {
								"type" : "keyword",
								"ignore_above" : 256
							}
						}
		              }
	                }
	              },
	              "contracts" : {
	                "type": "nested",
	                "properties" : {
	                  "amendments" : {
	                    "properties" : {
	                      "amendsReleaseID" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "date" : {
	                        "type" : "date"
	                      },
	                      "description" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "id" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "rationale" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "releaseID" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "awardID" : {
	                    "type" : "text"
	                  },
	                  "buyer" : {
	                    "properties" : {
	                      "id" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "name" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "dateSigned" : {
	                    "type" : "date"
	                  },
	                  "description" : {
	                    "type" : "text",
	                    "fields" : {
	                      "keyword" : {
	                        "type" : "keyword",
	                        "ignore_above" : 256
	                      }
	                    }
	                  },
	                  "documents" : {
	                    "properties" : {
	                      "dateModified" : {
	                        "type" : "date"
	                      },
	                      "datePublished" : {
	                        "type" : "date"
	                      },
	                      "description" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "documentType" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "id" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "title" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "url" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "guarantees" : {
	                    "properties" : {
	                      "guaranteePeriod" : {
	                        "properties" : {
	                          "endDate" : {
	                            "type" : "date"
	                          },
	                          "startDate" : {
	                            "type" : "date"
	                          }
	                        }
	                      },
	                      "guaranteeType" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "guaranteedObligations" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "guarantor" : {
	                        "properties" : {
	                          "id" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "name" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          }
	                        }
	                      },
	                      "id" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "value" : {
	                        "properties" : {
	                          "amount" : {
	                            "type" : "float"
	                          },
	                          "currency" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "id" : {
	                    "type" : "text",
	                    "fields" : {
	                      "keyword" : {
	                        "type" : "keyword",
	                        "ignore_above" : 256
	                      }
	                    }
	                  },
	                  "implementation" : {
	                    "properties" : {
	                      "financialObligations" : {
	                        "properties" : {
	                          "approvalDate" : {
	                            "type" : "date"
	                          },
	                          "bill" : {
	                            "properties" : {
	                              "amount" : {
	                                "properties" : {
	                                  "amount" : {
	                                    "type" : "float"
	                                  },
	                                  "currency" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  }
	                                }
	                              },
	                              "date" : {
	                                "type" : "date"
	                              },
	                              "description" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "id" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "type" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              }
	                            }
	                          },
	                          "description" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "id" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "retentions" : {
	                            "properties" : {
	                              "amount" : {
	                                "properties" : {
	                                  "amount" : {
	                                    "type" : "float"
	                                  },
	                                  "currency" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  }
	                                }
	                              },
	                              "name" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              }
	                            }
	                          }
	                        }
	                      },
	                      "transactions" : {
	                        "properties" : {
	                          "budgetSources" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "date" : {
	                            "type" : "date"
	                          },
	                          "financialObligationIds" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "id" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "payee" : {
	                            "properties" : {
	                              "id" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "name" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              }
	                            }
	                          },
	                          "payer" : {
	                            "properties" : {
	                              "id" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "name" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              }
	                            }
	                          },
	                          "uri" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "properties" : {
	                              "amount" : {
	                                "type" : "float"
	                              },
	                              "currency" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              }
	                            }
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "items" : {
	                    "properties" : {
	                      "classification" : {
	                        "properties" : {
	                          "description" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "id" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "scheme" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          }
	                        }
	                      },
	                      "description" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "id" : {
	                        "type" : "long"
	                      },
	                      "quantity" : {
	                        "type" : "float"
	                      },
	                      "unit" : {
	                        "properties" : {
	                          "name" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "properties" : {
	                              "amount" : {
	                                "type" : "float"
	                              },
	                              "currency" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              }
	                            }
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "period" : {
	                    "properties" : {
	                      "endDate" : {
	                        "type" : "date"
	                      },
	                      "startDate" : {
	                        "type" : "date"
	                      }
	                    }
	                  },
	                  "status" : {
	                    "type" : "text",
	                    "fields" : {
	                      "keyword" : {
	                        "type" : "keyword",
	                        "ignore_above" : 256
	                      }
	                    }
	                  },
	                  "suppliers" : {
	                    "type": "nested",
	                    "include_in_parent": True,
	                    "properties" : {
	                      "id" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "name" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "title" : {
	                    "type" : "text",
	                    "fields" : {
	                      "keyword" : {
	                        "type" : "keyword",
	                        "ignore_above" : 256
	                      }
	                    }
	                  },
	                  "value" : {
	                    "properties" : {
	                      "amount" : {
	                        "type" : "float"
	                      },
	                      "currency" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      }
	                    }
	                  }
	                }
	              },
	              "date" : {
	                "type" : "date"
	              },
	              "id" : {
	                "type" : "text",
	                "fields" : {
	                  "keyword" : {
	                    "type" : "keyword",
	                    "ignore_above" : 256
	                  }
	                }
	              },
	              "initiationType" : {
	                "type" : "text",
	                "fields" : {
	                  "keyword" : {
	                    "type" : "keyword",
	                    "ignore_above" : 256
	                  }
	                }
	              },
	              "language" : {
	                "type" : "text",
	                "fields" : {
	                  "keyword" : {
	                    "type" : "keyword",
	                    "ignore_above" : 256
	                  }
	                }
	              },
	              "ocid" : {
	                "type" : "text",
	                "fields" : {
	                  "keyword" : {
	                    "type" : "keyword",
	                    "ignore_above" : 256
	                  }
	                }
	              },
	              "parties" : {
	                "type": "nested",
	                "properties" : {
	                  "address" : {
	                    "properties" : {
	                      "countryName" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "locality" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "postalCode" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "region" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "streetAddress" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "contactPoint" : {
	                    "properties" : {
	                      "email" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "faxNumber" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "name" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "telephone" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "url" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "id" : {
	                    "type" : "text",
	                    "fields" : {
	                      "keyword" : {
	                        "type" : "keyword",
	                        "ignore_above" : 256
	                      }
	                    }
	                  },
	                  "identifier" : {
	                    "properties" : {
	                      "id" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "legalName" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "scheme" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "uri" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "memberOf" : {
	                    "properties" : {
	                      "id" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "name" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "name" : {
	                    "type" : "text",
	                    "fields" : {
	                      "keyword" : {
	                        "type" : "keyword",
	                        "ignore_above" : 256
	                      }
	                    }
	                  },
	                  "roles" : {
	                    "type" : "text",
	                    "fields" : {
	                      "keyword" : {
	                        "type" : "keyword",
	                        "ignore_above" : 256
	                      }
	                    }
	                  }
	                }
	              },
	              "planning" : {
	                "properties" : {
	                  "budget" : {
	                    "properties" : {
	                      "amount" : {
	                        "properties" : {
	                          "amount" : {
	                            "type" : "float"
	                          },
	                          "currency" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          }
	                        }
	                      },
	                      "budgetBreakdown" : {
	                        "properties" : {
	                          "amount" : {
	                            "properties" : {
	                              "amount" : {
	                                "type" : "float"
	                              },
	                              "currency" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              }
	                            }
	                          },
	                          "classifications" : {
	                            "properties" : {
	                              "actividadObra" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "fuente" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "ga" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "gestion" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "institucion" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "objeto" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "organismo" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "programa" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "proyecto" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "subPrograma" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "trfBeneficiario" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "ue" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              }
	                            }
	                          },
	                          "description" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "id" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "measures" : {
	                            "properties" : {
	                              "ajusteComprometido" : {
	                                "type" : "float"
	                              },
	                              "ajustePrecomprometido" : {
	                                "type" : "float"
	                              },
	                              "comprometido" : {
	                                "type" : "float"
	                              },
	                              "precomprometido" : {
	                                "type" : "float"
	                              }
	                            }
	                          },
	                          "sourceParty" : {
	                            "properties" : {
	                              "id" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "name" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              }
	                            }
	                          }
	                        }
	                      },
	                      "id" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "rationale" : {
	                    "type" : "text",
	                    "fields" : {
	                      "keyword" : {
	                        "type" : "keyword",
	                        "ignore_above" : 256
	                      }
	                    }
	                  }
	                }
	              },
	              "publisher" : {
	                "properties" : {
	                  "name" : {
	                    "type" : "text",
	                    "fields" : {
	                      "keyword" : {
	                        "type" : "keyword",
	                        "ignore_above" : 256
	                      }
	                    }
	                  }
	                }
	              },
	              "sources" : {
	                "properties" : {
	                  "id" : {
	                    "type" : "text",
	                    "fields" : {
	                      "keyword" : {
	                        "type" : "keyword",
	                        "ignore_above" : 256
	                      }
	                    }
	                  },
	                  "name" : {
	                    "type" : "text",
	                    "fields" : {
	                      "keyword" : {
	                        "type" : "keyword",
	                        "ignore_above" : 256
	                      }
	                    }
	                  },
	                  "url" : {
	                    "type" : "text",
	                    "fields" : {
	                      "keyword" : {
	                        "type" : "keyword",
	                        "ignore_above" : 256
	                      }
	                    }
	                  }
	                }
	              },
	              "tag" : {
	                "type" : "text",
	                "fields" : {
	                  "keyword" : {
	                    "type" : "keyword",
	                    "ignore_above" : 256
	                  }
	                }
	              },
	              "tender" : {
	                "properties" : {
	                  "additionalProcurementCategories" : {
	                    "type" : "text",
	                    "fields" : {
	                      "keyword" : {
	                        "type" : "keyword",
	                        "ignore_above" : 256
	                      }
	                    }
	                  },
	                  "description" : {
	                    "type" : "text",
	                    "fields" : {
	                      "keyword" : {
	                        "type" : "keyword",
	                        "ignore_above" : 256
	                      }
	                    }
	                  },
	                  "documents" : {
	                    "properties" : {
	                      "datePublished" : {
	                        "type" : "date"
	                      },
	                      "description" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "documentType" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "id" : {
	                        "type" : "long"
	                      },
	                      "title" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "url" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "enquiryPeriod" : {
	                    "properties" : {
	                      "endDate" : {
	                        "type" : "date"
	                      },
	                      "startDate" : {
	                        "type" : "date"
	                      }
	                    }
	                  },
	                  "id" : {
	                    "type" : "text",
	                    "fields" : {
	                      "keyword" : {
	                        "type" : "keyword",
	                        "ignore_above" : 256
	                      }
	                    }
	                  },
	                  "items" : {
	                    "properties" : {
	                      "classification" : {
	                        "properties" : {
	                          "description" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "id" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "scheme" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          }
	                        }
	                      },
	                      "description" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "id" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "quantity" : {
	                        "type" : "float"
	                      },
	                      "unit" : {
	                        "properties" : {
	                          "name" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "mainProcurementCategory" : {
	                    "type" : "text",
	                    "fields" : {
	                      "keyword" : {
	                        "type" : "keyword",
	                        "ignore_above" : 256
	                      }
	                    }
	                  },
	                  "participationFees" : {
	                    "properties" : {
	                      "id" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "type" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "value" : {
	                        "properties" : {
	                          "amount" : {
	                            "type" : "float"
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "procurementMethod" : {
	                    "type" : "text",
	                    "fields" : {
	                      "keyword" : {
	                        "type" : "keyword",
	                        "ignore_above" : 256
	                      }
	                    }
	                  },
	                  "procurementMethodDetails" : {
						"type" : "text",
						"analyzer": "ngram_analyzer",
						"search_analyzer": "whitespace_analyzer",
						"fields" : {
							"keyword" : {
								"type" : "keyword",
								"ignore_above" : 256
							}
						}	
	                  },
	                  "procuringEntity" : {
	                    "properties" : {
	                      "id" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "name" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "status" : {
	                    "type" : "text",
	                    "fields" : {
	                      "keyword" : {
	                        "type" : "keyword",
	                        "ignore_above" : 256
	                      }
	                    }
	                  },
	                  "tenderPeriod" : {
	                    "properties" : {
	                      "endDate" : {
	                        "type" : "date"
	                      },
	                      "startDate" : {
	                        "type" : "date"
	                      }
	                    }
	                  },
	                  "tenderers" : {
	                    "properties" : {
	                      "id" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "name" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "title" : {
						"type" : "text",
						"analyzer": "ngram_analyzer",
						"search_analyzer": "whitespace_analyzer",
						"fields" : {
							"keyword" : {
								"type" : "keyword",
								"ignore_above" : 256
							}
						}	
	                  }
	                }
	              }
	            }
	          },
	          "ocid" : {
				"type" : "text",
				"analyzer": "ngram_analyzer",
				"search_analyzer": "whitespace_analyzer",
				"fields" : {
					"keyword" : {
						"type" : "keyword",
						"ignore_above" : 256
					}
				}	
	          },
	          "releases" : {
	            "properties" : {
	              "awards" : {
	                "properties" : {
	                  "description" : {
	                    "type" : "text",
	                    "fields" : {
	                      "keyword" : {
	                        "type" : "keyword",
	                        "ignore_above" : 256
	                      }
	                    }
	                  },
	                  "documents" : {
	                    "properties" : {
	                      "datePublished" : {
	                        "type" : "date"
	                      },
	                      "description" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "documentType" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "id" : {
	                        "type" : "long"
	                      },
	                      "title" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "url" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "id" : {
	                    "type" : "text"
	                  },
	                  "items" : {
	                    "properties" : {
	                      "classification" : {
	                        "properties" : {
	                          "description" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "id" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "scheme" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          }
	                        }
	                      },
	                      "description" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "id" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "quantity" : {
	                        "type" : "float"
	                      },
	                      "unit" : {
	                        "properties" : {
	                          "name" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "properties" : {
	                              "amount" : {
	                                "type" : "float"
	                              }
	                            }
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "suppliers" : {
	                    "properties" : {
	                      "id" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "name" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "title" : {
	                    "type" : "text",
	                    "fields" : {
	                      "keyword" : {
	                        "type" : "keyword",
	                        "ignore_above" : 256
	                      }
	                    }
	                  },
	                  "value" : {
	                    "properties" : {
	                      "amount" : {
	                        "type" : "float"
	                      },
	                      "currency" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      }
	                    }
	                  }
	                }
	              },
	              "buyer" : {
	                "properties" : {
	                  "id" : {
	                    "type" : "text",
	                    "fields" : {
	                      "keyword" : {
	                        "type" : "keyword",
	                        "ignore_above" : 256
	                      }
	                    }
	                  },
	                  "name" : {
	                    "type" : "text",
	                    "fields" : {
	                      "keyword" : {
	                        "type" : "keyword",
	                        "ignore_above" : 256
	                      }
	                    }
	                  }
	                }
	              },
	              "contracts" : {
	                "properties" : {
	                  "amendments" : {
	                    "properties" : {
	                      "amendsReleaseID" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "date" : {
	                        "type" : "date"
	                      },
	                      "description" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "id" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "rationale" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "releaseID" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "awardID" : {
	                    "type" : "text"
	                  },
	                  "buyer" : {
	                    "properties" : {
	                      "id" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "name" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "dateSigned" : {
	                    "type" : "date"
	                  },
	                  "description" : {
	                    "type" : "text",
	                    "fields" : {
	                      "keyword" : {
	                        "type" : "keyword",
	                        "ignore_above" : 256
	                      }
	                    }
	                  },
	                  "documents" : {
	                    "properties" : {
	                      "dateModified" : {
	                        "type" : "date"
	                      },
	                      "datePublished" : {
	                        "type" : "date"
	                      },
	                      "description" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "documentType" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "id" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "title" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "url" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "guarantees" : {
	                    "properties" : {
	                      "guaranteePeriod" : {
	                        "properties" : {
	                          "endDate" : {
	                            "type" : "date"
	                          },
	                          "startDate" : {
	                            "type" : "date"
	                          }
	                        }
	                      },
	                      "guaranteeType" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "guaranteedObligations" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "guarantor" : {
	                        "properties" : {
	                          "id" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "name" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          }
	                        }
	                      },
	                      "id" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "value" : {
	                        "properties" : {
	                          "amount" : {
	                            "type" : "float"
	                          },
	                          "currency" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "id" : {
	                    "type" : "text"
	                  },
	                  "implementation" : {
	                    "properties" : {
	                      "financialObligations" : {
	                        "properties" : {
	                          "approvalDate" : {
	                            "type" : "date"
	                          },
	                          "bill" : {
	                            "properties" : {
	                              "amount" : {
	                                "properties" : {
	                                  "amount" : {
	                                    "type" : "float"
	                                  },
	                                  "currency" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  }
	                                }
	                              },
	                              "date" : {
	                                "type" : "date"
	                              },
	                              "description" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "id" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "type" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              }
	                            }
	                          },
	                          "description" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "id" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "retentions" : {
	                            "properties" : {
	                              "amount" : {
	                                "properties" : {
	                                  "amount" : {
	                                    "type" : "float"
	                                  },
	                                  "currency" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  }
	                                }
	                              },
	                              "name" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              }
	                            }
	                          }
	                        }
	                      },
	                      "transactions" : {
	                        "properties" : {
	                          "budgetSources" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "date" : {
	                            "type" : "date"
	                          },
	                          "financialObligationIds" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "id" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "payee" : {
	                            "properties" : {
	                              "id" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "name" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              }
	                            }
	                          },
	                          "payer" : {
	                            "properties" : {
	                              "id" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "name" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              }
	                            }
	                          },
	                          "uri" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "properties" : {
	                              "amount" : {
	                                "type" : "float"
	                              },
	                              "currency" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              }
	                            }
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "items" : {
	                    "properties" : {
	                      "classification" : {
	                        "properties" : {
	                          "description" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "id" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "scheme" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          }
	                        }
	                      },
	                      "description" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "id" : {
	                        "type" : "long"
	                      },
	                      "quantity" : {
	                        "type" : "float"
	                      },
	                      "unit" : {
	                        "properties" : {
	                          "name" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "properties" : {
	                              "amount" : {
	                                "type" : "float"
	                              },
	                              "currency" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              }
	                            }
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "period" : {
	                    "properties" : {
	                      "endDate" : {
	                        "type" : "date"
	                      },
	                      "startDate" : {
	                        "type" : "date"
	                      }
	                    }
	                  },
	                  "status" : {
	                    "type" : "text",
	                    "fields" : {
	                      "keyword" : {
	                        "type" : "keyword",
	                        "ignore_above" : 256
	                      }
	                    }
	                  },
	                  "suppliers" : {
	                    "properties" : {
	                      "id" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "name" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "title" : {
	                    "type" : "text",
	                    "fields" : {
	                      "keyword" : {
	                        "type" : "keyword",
	                        "ignore_above" : 256
	                      }
	                    }
	                  },
	                  "value" : {
	                    "properties" : {
	                      "amount" : {
	                        "type" : "float"
	                      },
	                      "currency" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      }
	                    }
	                  }
	                }
	              },
	              "date" : {
	                "type" : "date"
	              },
	              "id" : {
	                "type" : "text",
	                "fields" : {
	                  "keyword" : {
	                    "type" : "keyword",
	                    "ignore_above" : 256
	                  }
	                }
	              },
	              "initiationType" : {
	                "type" : "text",
	                "fields" : {
	                  "keyword" : {
	                    "type" : "keyword",
	                    "ignore_above" : 256
	                  }
	                }
	              },
	              "language" : {
	                "type" : "text",
	                "fields" : {
	                  "keyword" : {
	                    "type" : "keyword",
	                    "ignore_above" : 256
	                  }
	                }
	              },
	              "ocid" : {
	                "type" : "text",
	                "fields" : {
	                  "keyword" : {
	                    "type" : "keyword",
	                    "ignore_above" : 256
	                  }
	                }
	              },
	              "parties" : {
	                "properties" : {
	                  "address" : {
	                    "properties" : {
	                      "countryName" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "locality" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "postalCode" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "region" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "streetAddress" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "contactPoint" : {
	                    "properties" : {
	                      "email" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "faxNumber" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "name" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "telephone" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "url" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "id" : {
	                    "type" : "text",
	                    "fields" : {
	                      "keyword" : {
	                        "type" : "keyword",
	                        "ignore_above" : 256
	                      }
	                    }
	                  },
	                  "identifier" : {
	                    "properties" : {
	                      "id" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "legalName" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "scheme" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "uri" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "memberOf" : {
	                    "properties" : {
	                      "id" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "name" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "name" : {
	                    "type" : "text",
	                    "fields" : {
	                      "keyword" : {
	                        "type" : "keyword",
	                        "ignore_above" : 256
	                      }
	                    }
	                  },
	                  "roles" : {
	                    "type" : "text",
	                    "fields" : {
	                      "keyword" : {
	                        "type" : "keyword",
	                        "ignore_above" : 256
	                      }
	                    }
	                  }
	                }
	              },
	              "planning" : {
	                "properties" : {
	                  "budget" : {
	                    "properties" : {
	                      "amount" : {
	                        "properties" : {
	                          "amount" : {
	                            "type" : "float"
	                          },
	                          "currency" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          }
	                        }
	                      },
	                      "budgetBreakdown" : {
	                        "properties" : {
	                          "amount" : {
	                            "properties" : {
	                              "amount" : {
	                                "type" : "float"
	                              },
	                              "currency" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              }
	                            }
	                          },
	                          "classifications" : {
	                            "properties" : {
	                              "actividadObra" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "fuente" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "ga" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "gestion" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "institucion" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "objeto" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "organismo" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "programa" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "proyecto" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "subPrograma" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "trfBeneficiario" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "ue" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              }
	                            }
	                          },
	                          "description" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "id" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "measures" : {
	                            "properties" : {
	                              "ajusteComprometido" : {
	                                "type" : "float"
	                              },
	                              "ajustePrecomprometido" : {
	                                "type" : "float"
	                              },
	                              "comprometido" : {
	                                "type" : "float"
	                              },
	                              "precomprometido" : {
	                                "type" : "float"
	                              }
	                            }
	                          },
	                          "sourceParty" : {
	                            "properties" : {
	                              "id" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "name" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              }
	                            }
	                          }
	                        }
	                      },
	                      "id" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "rationale" : {
	                    "type" : "text",
	                    "fields" : {
	                      "keyword" : {
	                        "type" : "keyword",
	                        "ignore_above" : 256
	                      }
	                    }
	                  }
	                }
	              },
	              "publisher" : {
	                "properties" : {
	                  "name" : {
	                    "type" : "text",
	                    "fields" : {
	                      "keyword" : {
	                        "type" : "keyword",
	                        "ignore_above" : 256
	                      }
	                    }
	                  }
	                }
	              },
	              "sources" : {
	                "properties" : {
	                  "id" : {
	                    "type" : "text",
	                    "fields" : {
	                      "keyword" : {
	                        "type" : "keyword",
	                        "ignore_above" : 256
	                      }
	                    }
	                  },
	                  "name" : {
	                    "type" : "text",
	                    "fields" : {
	                      "keyword" : {
	                        "type" : "keyword",
	                        "ignore_above" : 256
	                      }
	                    }
	                  },
	                  "url" : {
	                    "type" : "text",
	                    "fields" : {
	                      "keyword" : {
	                        "type" : "keyword",
	                        "ignore_above" : 256
	                      }
	                    }
	                  }
	                }
	              },
	              "tag" : {
	                "type" : "text",
	                "fields" : {
	                  "keyword" : {
	                    "type" : "keyword",
	                    "ignore_above" : 256
	                  }
	                }
	              },
	              "tender" : {
	                "properties" : {
	                  "additionalProcurementCategories" : {
	                    "type" : "text",
	                    "fields" : {
	                      "keyword" : {
	                        "type" : "keyword",
	                        "ignore_above" : 256
	                      }
	                    }
	                  },
	                  "description" : {
	                    "type" : "text",
	                    "fields" : {
	                      "keyword" : {
	                        "type" : "keyword",
	                        "ignore_above" : 256
	                      }
	                    }
	                  },
	                  "documents" : {
	                    "properties" : {
	                      "datePublished" : {
	                        "type" : "date"
	                      },
	                      "description" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "documentType" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "id" : {
	                        "type" : "long"
	                      },
	                      "title" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "url" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "enquiryPeriod" : {
	                    "properties" : {
	                      "endDate" : {
	                        "type" : "date"
	                      },
	                      "startDate" : {
	                        "type" : "date"
	                      }
	                    }
	                  },
	                  "id" : {
	                    "type" : "text",
	                    "fields" : {
	                      "keyword" : {
	                        "type" : "keyword",
	                        "ignore_above" : 256
	                      }
	                    }
	                  },
	                  "items" : {
	                    "properties" : {
	                      "classification" : {
	                        "properties" : {
	                          "description" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "id" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "scheme" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          }
	                        }
	                      },
	                      "description" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "id" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "quantity" : {
	                        "type" : "float"
	                      },
	                      "unit" : {
	                        "properties" : {
	                          "name" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "mainProcurementCategory" : {
	                    "type" : "text",
	                    "fields" : {
	                      "keyword" : {
	                        "type" : "keyword",
	                        "ignore_above" : 256
	                      }
	                    }
	                  },
	                  "participationFees" : {
	                    "properties" : {
	                      "id" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "type" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "value" : {
	                        "properties" : {
	                          "amount" : {
	                            "type" : "float"
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "procurementMethod" : {
	                    "type" : "text",
	                    "fields" : {
	                      "keyword" : {
	                        "type" : "keyword",
	                        "ignore_above" : 256
	                      }
	                    }
	                  },
	                  "procurementMethodDetails" : {
	                    "type" : "text",
	                    "fields" : {
	                      "keyword" : {
	                        "type" : "keyword",
	                        "ignore_above" : 256
	                      }
	                    }
	                  },
	                  "procuringEntity" : {
	                    "properties" : {
	                      "id" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "name" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "status" : {
	                    "type" : "text",
	                    "fields" : {
	                      "keyword" : {
	                        "type" : "keyword",
	                        "ignore_above" : 256
	                      }
	                    }
	                  },
	                  "tenderPeriod" : {
	                    "properties" : {
	                      "endDate" : {
	                        "type" : "date"
	                      },
	                      "startDate" : {
	                        "type" : "date"
	                      }
	                    }
	                  },
	                  "tenderers" : {
	                    "properties" : {
	                      "id" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "name" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "title" : {
	                    "type" : "text",
	                    "fields" : {
	                      "keyword" : {
	                        "type" : "keyword",
	                        "ignore_above" : 256
	                      }
	                    }
	                  }
	                }
	              }
	            }
	          },
	          "versionedRelease" : {
	            "properties" : {
	              "awards" : {
	                "properties" : {
	                  "description" : {
	                    "properties" : {
	                      "releaseDate" : {
	                        "type" : "date"
	                      },
	                      "releaseID" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "releaseTag" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "value" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "documents" : {
	                    "properties" : {
	                      "datePublished" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "date"
	                          }
	                        }
	                      },
	                      "description" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          }
	                        }
	                      },
	                      "documentType" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          }
	                        }
	                      },
	                      "id" : {
	                        "type" : "long"
	                      },
	                      "title" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          }
	                        }
	                      },
	                      "url" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "id" : {
	                    "type" : "text"
	                  },
	                  "items" : {
	                    "properties" : {
	                      "classification" : {
	                        "properties" : {
	                          "description" : {
	                            "properties" : {
	                              "releaseDate" : {
	                                "type" : "date"
	                              },
	                              "releaseID" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "releaseTag" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "value" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              }
	                            }
	                          },
	                          "id" : {
	                            "properties" : {
	                              "releaseDate" : {
	                                "type" : "date"
	                              },
	                              "releaseID" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "releaseTag" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "value" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              }
	                            }
	                          },
	                          "scheme" : {
	                            "properties" : {
	                              "releaseDate" : {
	                                "type" : "date"
	                              },
	                              "releaseID" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "releaseTag" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "value" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              }
	                            }
	                          }
	                        }
	                      },
	                      "description" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          }
	                        }
	                      },
	                      "id" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "quantity" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "float"
	                          }
	                        }
	                      },
	                      "unit" : {
	                        "properties" : {
	                          "name" : {
	                            "properties" : {
	                              "releaseDate" : {
	                                "type" : "date"
	                              },
	                              "releaseID" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "releaseTag" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "value" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              }
	                            }
	                          },
	                          "value" : {
	                            "properties" : {
	                              "amount" : {
	                                "properties" : {
	                                  "releaseDate" : {
	                                    "type" : "date"
	                                  },
	                                  "releaseID" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "releaseTag" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "value" : {
	                                    "type" : "float"
	                                  }
	                                }
	                              }
	                            }
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "suppliers" : {
	                    "properties" : {
	                      "id" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "name" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "title" : {
	                    "properties" : {
	                      "releaseDate" : {
	                        "type" : "date"
	                      },
	                      "releaseID" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "releaseTag" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "value" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "value" : {
	                    "properties" : {
	                      "amount" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "float"
	                          }
	                        }
	                      },
	                      "currency" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          }
	                        }
	                      }
	                    }
	                  }
	                }
	              },
	              "buyer" : {
	                "properties" : {
	                  "id" : {
	                    "properties" : {
	                      "releaseDate" : {
	                        "type" : "date"
	                      },
	                      "releaseID" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "releaseTag" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "value" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "name" : {
	                    "properties" : {
	                      "releaseDate" : {
	                        "type" : "date"
	                      },
	                      "releaseID" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "releaseTag" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "value" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      }
	                    }
	                  }
	                }
	              },
	              "contracts" : {
	                "properties" : {
	                  "amendments" : {
	                    "properties" : {
	                      "amendsReleaseID" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          }
	                        }
	                      },
	                      "date" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "date"
	                          }
	                        }
	                      },
	                      "description" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          }
	                        }
	                      },
	                      "id" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "rationale" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          }
	                        }
	                      },
	                      "releaseID" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "awardID" : {
	                    "properties" : {
	                      "releaseDate" : {
	                        "type" : "date"
	                      },
	                      "releaseID" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "releaseTag" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "value" : {
	                        "type" : "text"
	                      }
	                    }
	                  },
	                  "buyer" : {
	                    "properties" : {
	                      "id" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          }
	                        }
	                      },
	                      "name" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "dateSigned" : {
	                    "properties" : {
	                      "releaseDate" : {
	                        "type" : "date"
	                      },
	                      "releaseID" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "releaseTag" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "value" : {
	                        "type" : "date"
	                      }
	                    }
	                  },
	                  "description" : {
	                    "properties" : {
	                      "releaseDate" : {
	                        "type" : "date"
	                      },
	                      "releaseID" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "releaseTag" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "value" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "documents" : {
	                    "properties" : {
	                      "dateModified" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "date"
	                          }
	                        }
	                      },
	                      "datePublished" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "date"
	                          }
	                        }
	                      },
	                      "description" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          }
	                        }
	                      },
	                      "documentType" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          }
	                        }
	                      },
	                      "id" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "title" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          }
	                        }
	                      },
	                      "url" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "guarantees" : {
	                    "properties" : {
	                      "guaranteePeriod" : {
	                        "properties" : {
	                          "endDate" : {
	                            "properties" : {
	                              "releaseDate" : {
	                                "type" : "date"
	                              },
	                              "releaseID" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "releaseTag" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "value" : {
	                                "type" : "date"
	                              }
	                            }
	                          },
	                          "startDate" : {
	                            "properties" : {
	                              "releaseDate" : {
	                                "type" : "date"
	                              },
	                              "releaseID" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "releaseTag" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "value" : {
	                                "type" : "date"
	                              }
	                            }
	                          }
	                        }
	                      },
	                      "guaranteeType" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          }
	                        }
	                      },
	                      "guaranteedObligations" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          }
	                        }
	                      },
	                      "guarantor" : {
	                        "properties" : {
	                          "id" : {
	                            "properties" : {
	                              "releaseDate" : {
	                                "type" : "date"
	                              },
	                              "releaseID" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "releaseTag" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "value" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              }
	                            }
	                          },
	                          "name" : {
	                            "properties" : {
	                              "releaseDate" : {
	                                "type" : "date"
	                              },
	                              "releaseID" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "releaseTag" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "value" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              }
	                            }
	                          }
	                        }
	                      },
	                      "id" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "value" : {
	                        "properties" : {
	                          "amount" : {
	                            "properties" : {
	                              "releaseDate" : {
	                                "type" : "date"
	                              },
	                              "releaseID" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "releaseTag" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "value" : {
	                                "type" : "float"
	                              }
	                            }
	                          },
	                          "currency" : {
	                            "properties" : {
	                              "releaseDate" : {
	                                "type" : "date"
	                              },
	                              "releaseID" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "releaseTag" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "value" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              }
	                            }
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "id" : {
	                    "type" : "text"
	                  },
	                  "implementation" : {
	                    "properties" : {
	                      "financialObligations" : {
	                        "properties" : {
	                          "approvalDate" : {
	                            "properties" : {
	                              "releaseDate" : {
	                                "type" : "date"
	                              },
	                              "releaseID" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "releaseTag" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "value" : {
	                                "type" : "date"
	                              }
	                            }
	                          },
	                          "bill" : {
	                            "properties" : {
	                              "amount" : {
	                                "properties" : {
	                                  "amount" : {
	                                    "properties" : {
	                                      "releaseDate" : {
	                                        "type" : "date"
	                                      },
	                                      "releaseID" : {
	                                        "type" : "text",
	                                        "fields" : {
	                                          "keyword" : {
	                                            "type" : "keyword",
	                                            "ignore_above" : 256
	                                          }
	                                        }
	                                      },
	                                      "releaseTag" : {
	                                        "type" : "text",
	                                        "fields" : {
	                                          "keyword" : {
	                                            "type" : "keyword",
	                                            "ignore_above" : 256
	                                          }
	                                        }
	                                      },
	                                      "value" : {
	                                        "type" : "float"
	                                      }
	                                    }
	                                  },
	                                  "currency" : {
	                                    "properties" : {
	                                      "releaseDate" : {
	                                        "type" : "date"
	                                      },
	                                      "releaseID" : {
	                                        "type" : "text",
	                                        "fields" : {
	                                          "keyword" : {
	                                            "type" : "keyword",
	                                            "ignore_above" : 256
	                                          }
	                                        }
	                                      },
	                                      "releaseTag" : {
	                                        "type" : "text",
	                                        "fields" : {
	                                          "keyword" : {
	                                            "type" : "keyword",
	                                            "ignore_above" : 256
	                                          }
	                                        }
	                                      },
	                                      "value" : {
	                                        "type" : "text",
	                                        "fields" : {
	                                          "keyword" : {
	                                            "type" : "keyword",
	                                            "ignore_above" : 256
	                                          }
	                                        }
	                                      }
	                                    }
	                                  }
	                                }
	                              },
	                              "date" : {
	                                "properties" : {
	                                  "releaseDate" : {
	                                    "type" : "date"
	                                  },
	                                  "releaseID" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "releaseTag" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "value" : {
	                                    "type" : "date"
	                                  }
	                                }
	                              },
	                              "description" : {
	                                "properties" : {
	                                  "releaseDate" : {
	                                    "type" : "date"
	                                  },
	                                  "releaseID" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "releaseTag" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "value" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  }
	                                }
	                              },
	                              "id" : {
	                                "properties" : {
	                                  "releaseDate" : {
	                                    "type" : "date"
	                                  },
	                                  "releaseID" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "releaseTag" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "value" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  }
	                                }
	                              },
	                              "type" : {
	                                "properties" : {
	                                  "releaseDate" : {
	                                    "type" : "date"
	                                  },
	                                  "releaseID" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "releaseTag" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "value" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  }
	                                }
	                              }
	                            }
	                          },
	                          "description" : {
	                            "properties" : {
	                              "releaseDate" : {
	                                "type" : "date"
	                              },
	                              "releaseID" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "releaseTag" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "value" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              }
	                            }
	                          },
	                          "id" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "retentions" : {
	                            "properties" : {
	                              "amount" : {
	                                "properties" : {
	                                  "amount" : {
	                                    "properties" : {
	                                      "releaseDate" : {
	                                        "type" : "date"
	                                      },
	                                      "releaseID" : {
	                                        "type" : "text",
	                                        "fields" : {
	                                          "keyword" : {
	                                            "type" : "keyword",
	                                            "ignore_above" : 256
	                                          }
	                                        }
	                                      },
	                                      "releaseTag" : {
	                                        "type" : "text",
	                                        "fields" : {
	                                          "keyword" : {
	                                            "type" : "keyword",
	                                            "ignore_above" : 256
	                                          }
	                                        }
	                                      },
	                                      "value" : {
	                                        "type" : "float"
	                                      }
	                                    }
	                                  },
	                                  "currency" : {
	                                    "properties" : {
	                                      "releaseDate" : {
	                                        "type" : "date"
	                                      },
	                                      "releaseID" : {
	                                        "type" : "text",
	                                        "fields" : {
	                                          "keyword" : {
	                                            "type" : "keyword",
	                                            "ignore_above" : 256
	                                          }
	                                        }
	                                      },
	                                      "releaseTag" : {
	                                        "type" : "text",
	                                        "fields" : {
	                                          "keyword" : {
	                                            "type" : "keyword",
	                                            "ignore_above" : 256
	                                          }
	                                        }
	                                      },
	                                      "value" : {
	                                        "type" : "text",
	                                        "fields" : {
	                                          "keyword" : {
	                                            "type" : "keyword",
	                                            "ignore_above" : 256
	                                          }
	                                        }
	                                      }
	                                    }
	                                  }
	                                }
	                              },
	                              "name" : {
	                                "properties" : {
	                                  "releaseDate" : {
	                                    "type" : "date"
	                                  },
	                                  "releaseID" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "releaseTag" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "value" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  }
	                                }
	                              }
	                            }
	                          }
	                        }
	                      },
	                      "transactions" : {
	                        "properties" : {
	                          "budgetSources" : {
	                            "properties" : {
	                              "releaseDate" : {
	                                "type" : "date"
	                              },
	                              "releaseID" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "releaseTag" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "value" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              }
	                            }
	                          },
	                          "date" : {
	                            "properties" : {
	                              "releaseDate" : {
	                                "type" : "date"
	                              },
	                              "releaseID" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "releaseTag" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "value" : {
	                                "type" : "date"
	                              }
	                            }
	                          },
	                          "financialObligationIds" : {
	                            "properties" : {
	                              "releaseDate" : {
	                                "type" : "date"
	                              },
	                              "releaseID" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "releaseTag" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "value" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              }
	                            }
	                          },
	                          "id" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "payee" : {
	                            "properties" : {
	                              "id" : {
	                                "properties" : {
	                                  "releaseDate" : {
	                                    "type" : "date"
	                                  },
	                                  "releaseID" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "releaseTag" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "value" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  }
	                                }
	                              },
	                              "name" : {
	                                "properties" : {
	                                  "releaseDate" : {
	                                    "type" : "date"
	                                  },
	                                  "releaseID" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "releaseTag" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "value" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  }
	                                }
	                              }
	                            }
	                          },
	                          "payer" : {
	                            "properties" : {
	                              "id" : {
	                                "properties" : {
	                                  "releaseDate" : {
	                                    "type" : "date"
	                                  },
	                                  "releaseID" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "releaseTag" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "value" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  }
	                                }
	                              },
	                              "name" : {
	                                "properties" : {
	                                  "releaseDate" : {
	                                    "type" : "date"
	                                  },
	                                  "releaseID" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "releaseTag" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "value" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  }
	                                }
	                              }
	                            }
	                          },
	                          "uri" : {
	                            "properties" : {
	                              "releaseDate" : {
	                                "type" : "date"
	                              },
	                              "releaseID" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "releaseTag" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "value" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              }
	                            }
	                          },
	                          "value" : {
	                            "properties" : {
	                              "amount" : {
	                                "properties" : {
	                                  "releaseDate" : {
	                                    "type" : "date"
	                                  },
	                                  "releaseID" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "releaseTag" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "value" : {
	                                    "type" : "float"
	                                  }
	                                }
	                              },
	                              "currency" : {
	                                "properties" : {
	                                  "releaseDate" : {
	                                    "type" : "date"
	                                  },
	                                  "releaseID" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "releaseTag" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "value" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  }
	                                }
	                              }
	                            }
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "items" : {
	                    "properties" : {
	                      "classification" : {
	                        "properties" : {
	                          "description" : {
	                            "properties" : {
	                              "releaseDate" : {
	                                "type" : "date"
	                              },
	                              "releaseID" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "releaseTag" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "value" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              }
	                            }
	                          },
	                          "id" : {
	                            "properties" : {
	                              "releaseDate" : {
	                                "type" : "date"
	                              },
	                              "releaseID" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "releaseTag" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "value" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              }
	                            }
	                          },
	                          "scheme" : {
	                            "properties" : {
	                              "releaseDate" : {
	                                "type" : "date"
	                              },
	                              "releaseID" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "releaseTag" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "value" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              }
	                            }
	                          }
	                        }
	                      },
	                      "description" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          }
	                        }
	                      },
	                      "id" : {
	                        "type" : "long"
	                      },
	                      "quantity" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "float"
	                          }
	                        }
	                      },
	                      "unit" : {
	                        "properties" : {
	                          "name" : {
	                            "properties" : {
	                              "releaseDate" : {
	                                "type" : "date"
	                              },
	                              "releaseID" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "releaseTag" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "value" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              }
	                            }
	                          },
	                          "value" : {
	                            "properties" : {
	                              "amount" : {
	                                "properties" : {
	                                  "releaseDate" : {
	                                    "type" : "date"
	                                  },
	                                  "releaseID" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "releaseTag" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "value" : {
	                                    "type" : "float"
	                                  }
	                                }
	                              },
	                              "currency" : {
	                                "properties" : {
	                                  "releaseDate" : {
	                                    "type" : "date"
	                                  },
	                                  "releaseID" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "releaseTag" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "value" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  }
	                                }
	                              }
	                            }
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "period" : {
	                    "properties" : {
	                      "endDate" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "date"
	                          }
	                        }
	                      },
	                      "startDate" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "date"
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "status" : {
	                    "properties" : {
	                      "releaseDate" : {
	                        "type" : "date"
	                      },
	                      "releaseID" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "releaseTag" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "value" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "suppliers" : {
	                    "properties" : {
	                      "id" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "name" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "title" : {
	                    "properties" : {
	                      "releaseDate" : {
	                        "type" : "date"
	                      },
	                      "releaseID" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "releaseTag" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "value" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "value" : {
	                    "properties" : {
	                      "amount" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "float"
	                          }
	                        }
	                      },
	                      "currency" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          }
	                        }
	                      }
	                    }
	                  }
	                }
	              },
	              "initiationType" : {
	                "properties" : {
	                  "releaseDate" : {
	                    "type" : "date"
	                  },
	                  "releaseID" : {
	                    "type" : "text",
	                    "fields" : {
	                      "keyword" : {
	                        "type" : "keyword",
	                        "ignore_above" : 256
	                      }
	                    }
	                  },
	                  "releaseTag" : {
	                    "type" : "text",
	                    "fields" : {
	                      "keyword" : {
	                        "type" : "keyword",
	                        "ignore_above" : 256
	                      }
	                    }
	                  },
	                  "value" : {
	                    "type" : "text",
	                    "fields" : {
	                      "keyword" : {
	                        "type" : "keyword",
	                        "ignore_above" : 256
	                      }
	                    }
	                  }
	                }
	              },
	              "language" : {
	                "properties" : {
	                  "releaseDate" : {
	                    "type" : "date"
	                  },
	                  "releaseID" : {
	                    "type" : "text",
	                    "fields" : {
	                      "keyword" : {
	                        "type" : "keyword",
	                        "ignore_above" : 256
	                      }
	                    }
	                  },
	                  "releaseTag" : {
	                    "type" : "text",
	                    "fields" : {
	                      "keyword" : {
	                        "type" : "keyword",
	                        "ignore_above" : 256
	                      }
	                    }
	                  },
	                  "value" : {
	                    "type" : "text",
	                    "fields" : {
	                      "keyword" : {
	                        "type" : "keyword",
	                        "ignore_above" : 256
	                      }
	                    }
	                  }
	                }
	              },
	              "ocid" : {
	                "type" : "text",
	                "fields" : {
	                  "keyword" : {
	                    "type" : "keyword",
	                    "ignore_above" : 256
	                  }
	                }
	              },
	              "parties" : {
	                "properties" : {
	                  "address" : {
	                    "properties" : {
	                      "countryName" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          }
	                        }
	                      },
	                      "locality" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          }
	                        }
	                      },
	                      "postalCode" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          }
	                        }
	                      },
	                      "region" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          }
	                        }
	                      },
	                      "releaseDate" : {
	                        "type" : "date"
	                      },
	                      "releaseID" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "releaseTag" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "streetAddress" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          }
	                        }
	                      },
	                      "value" : {
	                        "type" : "object"
	                      }
	                    }
	                  },
	                  "contactPoint" : {
	                    "properties" : {
	                      "email" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          }
	                        }
	                      },
	                      "faxNumber" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          }
	                        }
	                      },
	                      "name" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          }
	                        }
	                      },
	                      "releaseDate" : {
	                        "type" : "date"
	                      },
	                      "releaseID" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "releaseTag" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "telephone" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          }
	                        }
	                      },
	                      "url" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          }
	                        }
	                      },
	                      "value" : {
	                        "type" : "object"
	                      }
	                    }
	                  },
	                  "id" : {
	                    "type" : "text",
	                    "fields" : {
	                      "keyword" : {
	                        "type" : "keyword",
	                        "ignore_above" : 256
	                      }
	                    }
	                  },
	                  "identifier" : {
	                    "properties" : {
	                      "id" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          }
	                        }
	                      },
	                      "legalName" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          }
	                        }
	                      },
	                      "scheme" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          }
	                        }
	                      },
	                      "uri" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "memberOf" : {
	                    "properties" : {
	                      "id" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "name" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "name" : {
	                    "properties" : {
	                      "releaseDate" : {
	                        "type" : "date"
	                      },
	                      "releaseID" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "releaseTag" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "value" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "roles" : {
	                    "properties" : {
	                      "releaseDate" : {
	                        "type" : "date"
	                      },
	                      "releaseID" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "releaseTag" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "value" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      }
	                    }
	                  }
	                }
	              },
	              "planning" : {
	                "properties" : {
	                  "budget" : {
	                    "properties" : {
	                      "amount" : {
	                        "properties" : {
	                          "amount" : {
	                            "properties" : {
	                              "releaseDate" : {
	                                "type" : "date"
	                              },
	                              "releaseID" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "releaseTag" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "value" : {
	                                "type" : "float"
	                              }
	                            }
	                          },
	                          "currency" : {
	                            "properties" : {
	                              "releaseDate" : {
	                                "type" : "date"
	                              },
	                              "releaseID" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "releaseTag" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "value" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              }
	                            }
	                          }
	                        }
	                      },
	                      "budgetBreakdown" : {
	                        "properties" : {
	                          "amount" : {
	                            "properties" : {
	                              "amount" : {
	                                "properties" : {
	                                  "releaseDate" : {
	                                    "type" : "date"
	                                  },
	                                  "releaseID" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "releaseTag" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "value" : {
	                                    "type" : "float"
	                                  }
	                                }
	                              },
	                              "currency" : {
	                                "properties" : {
	                                  "releaseDate" : {
	                                    "type" : "date"
	                                  },
	                                  "releaseID" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "releaseTag" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "value" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  }
	                                }
	                              }
	                            }
	                          },
	                          "classifications" : {
	                            "properties" : {
	                              "actividadObra" : {
	                                "properties" : {
	                                  "releaseDate" : {
	                                    "type" : "date"
	                                  },
	                                  "releaseID" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "releaseTag" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "value" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  }
	                                }
	                              },
	                              "fuente" : {
	                                "properties" : {
	                                  "releaseDate" : {
	                                    "type" : "date"
	                                  },
	                                  "releaseID" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "releaseTag" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "value" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  }
	                                }
	                              },
	                              "ga" : {
	                                "properties" : {
	                                  "releaseDate" : {
	                                    "type" : "date"
	                                  },
	                                  "releaseID" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "releaseTag" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "value" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  }
	                                }
	                              },
	                              "gestion" : {
	                                "properties" : {
	                                  "releaseDate" : {
	                                    "type" : "date"
	                                  },
	                                  "releaseID" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "releaseTag" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "value" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  }
	                                }
	                              },
	                              "institucion" : {
	                                "properties" : {
	                                  "releaseDate" : {
	                                    "type" : "date"
	                                  },
	                                  "releaseID" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "releaseTag" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "value" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  }
	                                }
	                              },
	                              "objeto" : {
	                                "properties" : {
	                                  "releaseDate" : {
	                                    "type" : "date"
	                                  },
	                                  "releaseID" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "releaseTag" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "value" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  }
	                                }
	                              },
	                              "organismo" : {
	                                "properties" : {
	                                  "releaseDate" : {
	                                    "type" : "date"
	                                  },
	                                  "releaseID" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "releaseTag" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "value" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  }
	                                }
	                              },
	                              "programa" : {
	                                "properties" : {
	                                  "releaseDate" : {
	                                    "type" : "date"
	                                  },
	                                  "releaseID" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "releaseTag" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "value" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  }
	                                }
	                              },
	                              "proyecto" : {
	                                "properties" : {
	                                  "releaseDate" : {
	                                    "type" : "date"
	                                  },
	                                  "releaseID" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "releaseTag" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "value" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  }
	                                }
	                              },
	                              "subPrograma" : {
	                                "properties" : {
	                                  "releaseDate" : {
	                                    "type" : "date"
	                                  },
	                                  "releaseID" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "releaseTag" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "value" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  }
	                                }
	                              },
	                              "trfBeneficiario" : {
	                                "properties" : {
	                                  "releaseDate" : {
	                                    "type" : "date"
	                                  },
	                                  "releaseID" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "releaseTag" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "value" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  }
	                                }
	                              },
	                              "ue" : {
	                                "properties" : {
	                                  "releaseDate" : {
	                                    "type" : "date"
	                                  },
	                                  "releaseID" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "releaseTag" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "value" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  }
	                                }
	                              }
	                            }
	                          },
	                          "description" : {
	                            "properties" : {
	                              "releaseDate" : {
	                                "type" : "date"
	                              },
	                              "releaseID" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "releaseTag" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "value" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              }
	                            }
	                          },
	                          "id" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "measures" : {
	                            "properties" : {
	                              "ajusteComprometido" : {
	                                "properties" : {
	                                  "releaseDate" : {
	                                    "type" : "date"
	                                  },
	                                  "releaseID" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "releaseTag" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "value" : {
	                                    "type" : "float"
	                                  }
	                                }
	                              },
	                              "ajustePrecomprometido" : {
	                                "properties" : {
	                                  "releaseDate" : {
	                                    "type" : "date"
	                                  },
	                                  "releaseID" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "releaseTag" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "value" : {
	                                    "type" : "float"
	                                  }
	                                }
	                              },
	                              "comprometido" : {
	                                "properties" : {
	                                  "releaseDate" : {
	                                    "type" : "date"
	                                  },
	                                  "releaseID" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "releaseTag" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "value" : {
	                                    "type" : "float"
	                                  }
	                                }
	                              },
	                              "precomprometido" : {
	                                "properties" : {
	                                  "releaseDate" : {
	                                    "type" : "date"
	                                  },
	                                  "releaseID" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "releaseTag" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "value" : {
	                                    "type" : "float"
	                                  }
	                                }
	                              }
	                            }
	                          },
	                          "sourceParty" : {
	                            "properties" : {
	                              "id" : {
	                                "properties" : {
	                                  "releaseDate" : {
	                                    "type" : "date"
	                                  },
	                                  "releaseID" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "releaseTag" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "value" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  }
	                                }
	                              },
	                              "name" : {
	                                "properties" : {
	                                  "releaseDate" : {
	                                    "type" : "date"
	                                  },
	                                  "releaseID" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "releaseTag" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  },
	                                  "value" : {
	                                    "type" : "text",
	                                    "fields" : {
	                                      "keyword" : {
	                                        "type" : "keyword",
	                                        "ignore_above" : 256
	                                      }
	                                    }
	                                  }
	                                }
	                              }
	                            }
	                          }
	                        }
	                      },
	                      "id" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "rationale" : {
	                    "properties" : {
	                      "releaseDate" : {
	                        "type" : "date"
	                      },
	                      "releaseID" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "releaseTag" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "value" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      }
	                    }
	                  }
	                }
	              },
	              "publisher" : {
	                "properties" : {
	                  "name" : {
	                    "properties" : {
	                      "releaseDate" : {
	                        "type" : "date"
	                      },
	                      "releaseID" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "releaseTag" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "value" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      }
	                    }
	                  }
	                }
	              },
	              "sources" : {
	                "properties" : {
	                  "id" : {
	                    "type" : "text",
	                    "fields" : {
	                      "keyword" : {
	                        "type" : "keyword",
	                        "ignore_above" : 256
	                      }
	                    }
	                  },
	                  "name" : {
	                    "properties" : {
	                      "releaseDate" : {
	                        "type" : "date"
	                      },
	                      "releaseID" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "releaseTag" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "value" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "url" : {
	                    "properties" : {
	                      "releaseDate" : {
	                        "type" : "date"
	                      },
	                      "releaseID" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "releaseTag" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "value" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      }
	                    }
	                  }
	                }
	              },
	              "tender" : {
	                "properties" : {
	                  "additionalProcurementCategories" : {
	                    "properties" : {
	                      "releaseDate" : {
	                        "type" : "date"
	                      },
	                      "releaseID" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "releaseTag" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "value" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "description" : {
	                    "properties" : {
	                      "releaseDate" : {
	                        "type" : "date"
	                      },
	                      "releaseID" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "releaseTag" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "value" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "documents" : {
	                    "properties" : {
	                      "datePublished" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "date"
	                          }
	                        }
	                      },
	                      "description" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          }
	                        }
	                      },
	                      "documentType" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          }
	                        }
	                      },
	                      "id" : {
	                        "type" : "long"
	                      },
	                      "title" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          }
	                        }
	                      },
	                      "url" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "enquiryPeriod" : {
	                    "properties" : {
	                      "endDate" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "date"
	                          }
	                        }
	                      },
	                      "startDate" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "date"
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "id" : {
	                    "properties" : {
	                      "releaseDate" : {
	                        "type" : "date"
	                      },
	                      "releaseID" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "releaseTag" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "value" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "items" : {
	                    "properties" : {
	                      "classification" : {
	                        "properties" : {
	                          "description" : {
	                            "properties" : {
	                              "releaseDate" : {
	                                "type" : "date"
	                              },
	                              "releaseID" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "releaseTag" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "value" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              }
	                            }
	                          },
	                          "id" : {
	                            "properties" : {
	                              "releaseDate" : {
	                                "type" : "date"
	                              },
	                              "releaseID" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "releaseTag" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "value" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              }
	                            }
	                          },
	                          "scheme" : {
	                            "properties" : {
	                              "releaseDate" : {
	                                "type" : "date"
	                              },
	                              "releaseID" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "releaseTag" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "value" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              }
	                            }
	                          }
	                        }
	                      },
	                      "description" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          }
	                        }
	                      },
	                      "id" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "quantity" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "float"
	                          }
	                        }
	                      },
	                      "unit" : {
	                        "properties" : {
	                          "name" : {
	                            "properties" : {
	                              "releaseDate" : {
	                                "type" : "date"
	                              },
	                              "releaseID" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "releaseTag" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "value" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              }
	                            }
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "mainProcurementCategory" : {
	                    "properties" : {
	                      "releaseDate" : {
	                        "type" : "date"
	                      },
	                      "releaseID" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "releaseTag" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "value" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "participationFees" : {
	                    "properties" : {
	                      "id" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "type" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          }
	                        }
	                      },
	                      "value" : {
	                        "properties" : {
	                          "amount" : {
	                            "properties" : {
	                              "releaseDate" : {
	                                "type" : "date"
	                              },
	                              "releaseID" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "releaseTag" : {
	                                "type" : "text",
	                                "fields" : {
	                                  "keyword" : {
	                                    "type" : "keyword",
	                                    "ignore_above" : 256
	                                  }
	                                }
	                              },
	                              "value" : {
	                                "type" : "float"
	                              }
	                            }
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "procurementMethod" : {
	                    "properties" : {
	                      "releaseDate" : {
	                        "type" : "date"
	                      },
	                      "releaseID" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "releaseTag" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "value" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "procurementMethodDetails" : {
	                    "properties" : {
	                      "releaseDate" : {
	                        "type" : "date"
	                      },
	                      "releaseID" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "releaseTag" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "value" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "procuringEntity" : {
	                    "properties" : {
	                      "id" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          }
	                        }
	                      },
	                      "name" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "status" : {
	                    "properties" : {
	                      "releaseDate" : {
	                        "type" : "date"
	                      },
	                      "releaseID" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "releaseTag" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "value" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "tenderPeriod" : {
	                    "properties" : {
	                      "endDate" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "date"
	                          }
	                        }
	                      },
	                      "startDate" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "date"
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "tenderers" : {
	                    "properties" : {
	                      "id" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "name" : {
	                        "properties" : {
	                          "releaseDate" : {
	                            "type" : "date"
	                          },
	                          "releaseID" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "releaseTag" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          },
	                          "value" : {
	                            "type" : "text",
	                            "fields" : {
	                              "keyword" : {
	                                "type" : "keyword",
	                                "ignore_above" : 256
	                              }
	                            }
	                          }
	                        }
	                      }
	                    }
	                  },
	                  "title" : {
	                    "properties" : {
	                      "releaseDate" : {
	                        "type" : "date"
	                      },
	                      "releaseID" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "releaseTag" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      },
	                      "value" : {
	                        "type" : "text",
	                        "fields" : {
	                          "keyword" : {
	                            "type" : "keyword",
	                            "ignore_above" : 256
	                          }
	                        }
	                      }
	                    }
	                  }
	                }
	              }
	            }
	          }
	        }
	      },
          "extra" : {
          	"properties": {
		        "buyerFullName" : {
		            "type" : "text",
					"analyzer": "ngram_analyzer",
					"search_analyzer": "whitespace_analyzer",
					"fields" : {
						"keyword" : {
							"type" : "keyword",
							"ignore_above" : 256
						}
					}					
		        },		        
		        "parent1" : {
		            "properties" : {
		              "id" : {
		                "type" : "text",
		                "fields" : {
		                  "keyword" : {
		                    "type" : "keyword",
		                    "ignore_above" : 256
		                  }
		                }
		              },
		              "name" : {
						"type" : "text",
						"analyzer": "ngram_analyzer",
						"search_analyzer": "whitespace_analyzer"
		              }
		            }
		        },
		        "parent2" : {
		            "properties" : {
		              "id" : {
		                "type" : "text",
		                "fields" : {
		                  "keyword" : {
		                    "type" : "keyword",
		                    "ignore_above" : 256
		                  }
		                }
		              },
		              "name" : {
						"type" : "text",
						"analyzer": "ngram_analyzer",
						"search_analyzer": "whitespace_analyzer"
		              }
		            }
		        },
		        "parentTop" : {
		            "properties" : {
		              "id" : {
		                "type" : "text",
		                "fields" : {
		                  "keyword" : {
		                    "type" : "keyword",
		                    "ignore_above" : 256
		                  }
		                }
		              },
		              "name" : {
						"type" : "text",
						"analyzer": "ngram_analyzer",
						"search_analyzer": "whitespace_analyzer",
		                "fields" : {
		                  "keyword" : {
		                    "type" : "keyword",
		                    "ignore_above" : 256
		                  }
		                }						
		              }
		            }
		        },   		        
          	}
          }

	    }
	  }
	}

	settings = {
		"max_result_window": 500000,
		"index" : {
			"mapping" : {
				"total_fields" : {
					"limit" : "100000"
				}
			}
		},
		"analysis": {
			"filter": {
				"autocomplete_filter": {
					"type": "ngram", #edge_ngram
					"min_gram":2,
					"max_gram":20,
					"token_chars": [
						"letter",
						"digit",
						"punctuation",
						"symbol"
					]
				}
			},
			"analyzer": {
				"ngram_analyzer": {
					"type": "custom",
					"tokenizer": "whitespace", #standard
					"filter": [
						"lowercase", 
						"asciifolding",
						"autocomplete_filter"
					]
				},
				"whitespace_analyzer": {
					"type": "custom",
					"tokenizer": "whitespace",
					"filter": [
						"lowercase",
						"asciifolding"
					]
				}
			}
		}
	}

	contract_mapping = {
	  "contract":{
        "properties" : {
          "amendments" : {
            "properties" : {
              "amendsReleaseID" : {
                "type" : "text",
                "fields" : {
                  "keyword" : {
                    "type" : "keyword",
                    "ignore_above" : 256
                  }
                }
              },
              "date" : {
                "type" : "date"
              },
              "description" : {
                "type" : "text",
                "fields" : {
                  "keyword" : {
                    "type" : "keyword",
                    "ignore_above" : 256
                  }
                }
              },
              "id" : {
                "type" : "text",
                "fields" : {
                  "keyword" : {
                    "type" : "keyword",
                    "ignore_above" : 256
                  }
                }
              },
              "rationale" : {
                "type" : "text",
                "fields" : {
                  "keyword" : {
                    "type" : "keyword",
                    "ignore_above" : 256
                  }
                }
              },
              "releaseID" : {
                "type" : "text",
                "fields" : {
                  "keyword" : {
                    "type" : "keyword",
                    "ignore_above" : 256
                  }
                }
              }
            }
          },
          "awardID" : {
            "type" : "text"
          },
          "buyer" : {
            "properties" : {
              "id" : {
                "type" : "text",
                "fields" : {
                  "keyword" : {
                    "type" : "keyword",
                    "ignore_above" : 256
                  }
                }
              },
              "name" : {
				"type" : "text",
				"analyzer": "ngram_analyzer",
				"search_analyzer": "whitespace_analyzer",
				"fields" : {
					"keyword" : {
						"type" : "keyword",
						"ignore_above" : 256
					}
				}
              }
            }
          },
          "dateSigned" : {
            "type" : "date"
          },
          "description" : {
            "type" : "text",
            "fields" : {
              "keyword" : {
                "type" : "keyword",
                "ignore_above" : 256
              }
            }
          },
          "documents" : {
            "properties" : {
              "dateModified" : {
                "type" : "date"
              },
              "datePublished" : {
                "type" : "date"
              },
              "description" : {
                "type" : "text",
                "fields" : {
                  "keyword" : {
                    "type" : "keyword",
                    "ignore_above" : 256
                  }
                }
              },
              "documentType" : {
                "type" : "text",
                "fields" : {
                  "keyword" : {
                    "type" : "keyword",
                    "ignore_above" : 256
                  }
                }
              },
              "id" : {
                "type" : "text",
                "fields" : {
                  "keyword" : {
                    "type" : "keyword",
                    "ignore_above" : 256
                  }
                }
              },
              "title" : {
                "type" : "text",
                "fields" : {
                  "keyword" : {
                    "type" : "keyword",
                    "ignore_above" : 256
                  }
                }
              },
              "url" : {
                "type" : "text",
                "fields" : {
                  "keyword" : {
                    "type" : "keyword",
                    "ignore_above" : 256
                  }
                }
              }
            }
          },
          "guarantees" : {
            "properties" : {
              "guaranteePeriod" : {
                "properties" : {
                  "endDate" : {
                    "type" : "date"
                  },
                  "startDate" : {
                    "type" : "date"
                  }
                }
              },
              "guaranteeType" : {
                "type" : "text",
                "fields" : {
                  "keyword" : {
                    "type" : "keyword",
                    "ignore_above" : 256
                  }
                }
              },
              "guaranteedObligations" : {
                "type" : "text",
                "fields" : {
                  "keyword" : {
                    "type" : "keyword",
                    "ignore_above" : 256
                  }
                }
              },
              "guarantor" : {
                "properties" : {
                  "id" : {
                    "type" : "text",
                    "fields" : {
                      "keyword" : {
                        "type" : "keyword",
                        "ignore_above" : 256
                      }
                    }
                  },
                  "name" : {
                    "type" : "text",
                    "fields" : {
                      "keyword" : {
                        "type" : "keyword",
                        "ignore_above" : 256
                      }
                    }
                  }
                }
              },
              "id" : {
                "type" : "text",
                "fields" : {
                  "keyword" : {
                    "type" : "keyword",
                    "ignore_above" : 256
                  }
                }
              },
              "value" : {
                "properties" : {
                  "amount" : {
                    "type" : "float"
                  },
                  "currency" : {
                    "type" : "text",
                    "fields" : {
                      "keyword" : {
                        "type" : "keyword",
                        "ignore_above" : 256
                      }
                    }
                  }
                }
              }
            }
          },
          "id" : {
            "type" : "text",
            "fields" : {
              "keyword" : {
                "type" : "keyword",
                "ignore_above" : 256
              }
            }
          },
          "implementation" : {
            "properties" : {
              "financialObligations" : {
                "properties" : {
                  "approvalDate" : {
                    "type" : "date"
                  },
                  "bill" : {
                    "properties" : {
                      "amount" : {
                        "properties" : {
                          "amount" : {
                            "type" : "float"
                          },
                          "currency" : {
                            "type" : "text",
                            "fields" : {
                              "keyword" : {
                                "type" : "keyword",
                                "ignore_above" : 256
                              }
                            }
                          }
                        }
                      },
                      "date" : {
                        "type" : "date"
                      },
                      "description" : {
                        "type" : "text",
                        "fields" : {
                          "keyword" : {
                            "type" : "keyword",
                            "ignore_above" : 256
                          }
                        }
                      },
                      "id" : {
                        "type" : "text",
                        "fields" : {
                          "keyword" : {
                            "type" : "keyword",
                            "ignore_above" : 256
                          }
                        }
                      },
                      "type" : {
                        "type" : "text",
                        "fields" : {
                          "keyword" : {
                            "type" : "keyword",
                            "ignore_above" : 256
                          }
                        }
                      }
                    }
                  },
                  "description" : {
                    "type" : "text",
                    "fields" : {
                      "keyword" : {
                        "type" : "keyword",
                        "ignore_above" : 256
                      }
                    }
                  },
                  "id" : {
                    "type" : "text",
                    "fields" : {
                      "keyword" : {
                        "type" : "keyword",
                        "ignore_above" : 256
                      }
                    }
                  },
                  "retentions" : {
                    "properties" : {
                      "amount" : {
                        "properties" : {
                          "amount" : {
                            "type" : "float"
                          },
                          "currency" : {
                            "type" : "text",
                            "fields" : {
                              "keyword" : {
                                "type" : "keyword",
                                "ignore_above" : 256
                              }
                            }
                          }
                        }
                      },
                      "name" : {
                        "type" : "text",
                        "fields" : {
                          "keyword" : {
                            "type" : "keyword",
                            "ignore_above" : 256
                          }
                        }
                      }
                    }
                  }
                }
              },
              "transactions" : {
              	"type": "nested",
                "properties" : {
                  "budgetSources" : {
                    "type" : "text",
                    "fields" : {
                      "keyword" : {
                        "type" : "keyword",
                        "ignore_above" : 256
                      }
                    }
                  },
                  "date" : {
                    "type" : "date"
                  },
                  "financialObligationIds" : {
                    "type" : "text",
                    "fields" : {
                      "keyword" : {
                        "type" : "keyword",
                        "ignore_above" : 256
                      }
                    }
                  },
                  "id" : {
                    "type" : "text",
                    "fields" : {
                      "keyword" : {
                        "type" : "keyword",
                        "ignore_above" : 256
                      }
                    }
                  },
                  "payee" : {
                    "properties" : {
                      "id" : {
                        "type" : "text",
                        "fields" : {
                          "keyword" : {
                            "type" : "keyword",
                            "ignore_above" : 256
                          }
                        }
                      },
                      "name" : {
			            "type" : "text",
						"analyzer": "ngram_analyzer",
						"search_analyzer": "whitespace_analyzer",
						"fields" : {
							"keyword" : {
								"type" : "keyword",
								"ignore_above" : 256
							}
						}	
                      }
                    }
                  },
                  "payer" : {
                    "properties" : {
                      "id" : {
                        "type" : "text",
                        "fields" : {
                          "keyword" : {
                            "type" : "keyword",
                            "ignore_above" : 256
                          }
                        }
                      },
                      "name" : {
                        "type" : "text",
                        "fields" : {
                          "keyword" : {
                            "type" : "keyword",
                            "ignore_above" : 256
                          }
                        }
                      }
                    }
                  },
                  "uri" : {
                    "type" : "text",
                    "fields" : {
                      "keyword" : {
                        "type" : "keyword",
                        "ignore_above" : 256
                      }
                    }
                  },
                  "value" : {
                    "properties" : {
                      "amount" : {
                        "type" : "float"
                      },
                      "currency" : {
                        "type" : "text",
                        "fields" : {
                          "keyword" : {
                            "type" : "keyword",
                            "ignore_above" : 256
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          },
          "items" : {
            "properties" : {
              "classification" : {
                "properties" : {
                  "description" : {
		            "type" : "text",
					"analyzer": "ngram_analyzer",
					"search_analyzer": "whitespace_analyzer",
					"fields" : {
						"keyword" : {
							"type" : "keyword",
							"ignore_above" : 256
						}
					}	
                  },
                  "id" : {
                    "type" : "text",
                    "fields" : {
                      "keyword" : {
                        "type" : "keyword",
                        "ignore_above" : 256
                      }
                    }
                  },
                  "scheme" : {
                    "type" : "text",
                    "fields" : {
                      "keyword" : {
                        "type" : "keyword",
                        "ignore_above" : 256
                      }
                    }
                  }
                }
              },
              "description" : {
                "type" : "text",
                "fields" : {
                  "keyword" : {
                    "type" : "keyword",
                    "ignore_above" : 256
                  }
                }
              },
              "id" : {
                "type" : "long"
              },
              "quantity" : {
                "type" : "float"
              },
              "unit" : {
                "properties" : {
                  "name" : {
                    "type" : "text",
                    "fields" : {
                      "keyword" : {
                        "type" : "keyword",
                        "ignore_above" : 256
                      }
                    }
                  },
                  "value" : {
                    "properties" : {
                      "amount" : {
                        "type" : "float"
                      },
                      "currency" : {
                        "type" : "text",
                        "fields" : {
                          "keyword" : {
                            "type" : "keyword",
                            "ignore_above" : 256
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          },
          "period" : {
            "properties" : {
              "endDate" : {
                "type" : "date"
              },
              "startDate" : {
                "type" : "date"
              }
            }
          },
          "status" : {
            "type" : "text",
            "fields" : {
              "keyword" : {
                "type" : "keyword",
                "ignore_above" : 256
              }
            }
          },
          "suppliers" : {
            "type": "nested",
            "include_in_parent": True,
            "properties" : {
              "id" : {
                "type" : "text",
                "fields" : {
                  "keyword" : {
                    "type" : "keyword",
                    "ignore_above" : 256
                  }
                }
              },
              "name" : {
                "type" : "text",
                "fields" : {
                  "keyword" : {
                    "type" : "keyword",
                    "ignore_above" : 256
                  }
                }
              }
            }
          },
          "title" : {
            "type" : "text",
			"analyzer": "ngram_analyzer",
			"search_analyzer": "whitespace_analyzer",
			"fields" : {
				"keyword" : {
					"type" : "keyword",
					"ignore_above" : 256
				}
			}			
          },
          "value" : {
            "properties" : {
              "amount" : {
                "type" : "float"
              },
              "currency" : {
                "type" : "text",
                "fields" : {
                  "keyword" : {
                    "type" : "keyword",
                    "ignore_above" : 256
                  }
                }
              }
            }
          },
          "extra" : {
          	"properties": {
          		"tenderMainProcurementCategory": {
                	"type" : "text",
	                "fields" : {
	                  "keyword" : {
	                    "type" : "keyword",
	                    "ignore_above" : 256
	                  }
	                }
          		},
          		"tenderAdditionalProcurementCategories": {
                	"type" : "text",
	                "fields" : {
	                  "keyword" : {
	                    "type" : "keyword",
	                    "ignore_above" : 256
	                  }
	                }
          		},
		        "tenderTitle" : {
		            "type" : "text",
					"analyzer": "ngram_analyzer",
					"search_analyzer": "whitespace_analyzer",
					"fields" : {
						"keyword" : {
							"type" : "keyword",
							"ignore_above" : 256
						}
					}					
		        },
		        "buyerFullName" : {
		            "type" : "text",
					"analyzer": "ngram_analyzer",
					"search_analyzer": "whitespace_analyzer",
					"fields" : {
						"keyword" : {
							"type" : "keyword",
							"ignore_above" : 256
						}
					}					
		        },		        
		        "parent1" : {
		            "properties" : {
		              "id" : {
		                "type" : "text",
		                "fields" : {
		                  "keyword" : {
		                    "type" : "keyword",
		                    "ignore_above" : 256
		                  }
		                }
		              },
		              "name" : {
						"type" : "text",
						"analyzer": "ngram_analyzer",
						"search_analyzer": "whitespace_analyzer"
		              }
		            }
		        },
		        "parent2" : {
		            "properties" : {
		              "id" : {
		                "type" : "text",
		                "fields" : {
		                  "keyword" : {
		                    "type" : "keyword",
		                    "ignore_above" : 256
		                  }
		                }
		              },
		              "name" : {
						"type" : "text",
						"analyzer": "ngram_analyzer",
						"search_analyzer": "whitespace_analyzer"
		              }
		            }
		        },          	
          	}
          }
        }	  
	  }
	}

	transaction_mapping = {
		"transactions" : {
			"properties" : {
			  "budgetSources" : {
			    "type" : "text",
			    "fields" : {
			      "keyword" : {
			        "type" : "keyword",
			        "ignore_above" : 256
			      }
			    }
			  },
			  "date" : {
			    "type" : "date"
			  },
			  "financialObligationIds" : {
			    "type" : "text",
			    "fields" : {
			      "keyword" : {
			        "type" : "keyword",
			        "ignore_above" : 256
			      }
			    }
			  },
			  "id" : {
			    "type" : "text",
			    "fields" : {
			      "keyword" : {
			        "type" : "keyword",
			        "ignore_above" : 256
			      }
			    }
			  },
			  "payee" : {
			    "properties" : {
			      "id" : {
			        "type" : "text",
			        "fields" : {
			          "keyword" : {
			            "type" : "keyword",
			            "ignore_above" : 256
			          }
			        }
			      },
			      "name" : {
			        "type" : "text",
			        "fields" : {
			          "keyword" : {
			            "type" : "keyword",
			            "ignore_above" : 256
			          }
			        }
			      }
			    }
			  },
			  "payer" : {
			    "properties" : {
			      "id" : {
			        "type" : "text",
			        "fields" : {
			          "keyword" : {
			            "type" : "keyword",
			            "ignore_above" : 256
			          }
			        }
			      },
			      "name" : {
			        "type" : "text",
			        "fields" : {
			          "keyword" : {
			            "type" : "keyword",
			            "ignore_above" : 256
			          }
			        }
			      }
			    }
			  },
			  "uri" : {
			    "type" : "text",
			    "fields" : {
			      "keyword" : {
			        "type" : "keyword",
			        "ignore_above" : 256
			      }
			    }
			  },
			  "value" : {
			    "properties" : {
			      "amount" : {
			        "type" : "float"
			      },
			      "currency" : {
			        "type" : "text",
			        "fields" : {
			          "keyword" : {
			            "type" : "keyword",
			            "ignore_above" : 256
			          }
			        }
			      }
			    }
			  }
			}
		},
		"extra" : {
			"properties": {
				"buyerFullName" : {
					"type" : "text",
					"analyzer": "ngram_analyzer",
					"search_analyzer": "whitespace_analyzer",
					"fields" : {
						"keyword" : {
							"type" : "keyword",
							"ignore_above" : 256
						}
					}
				},
				"parent1" : {
					"properties" : {
					"id" : {
						"type" : "text",
						"fields" : {
							"keyword" : {
								"type" : "keyword",
								"ignore_above" : 256
							}
						}
					},
					"name" : {
						"type" : "text",
						"analyzer": "ngram_analyzer",
						"search_analyzer": "whitespace_analyzer"
					}
				}
				},
				"parent2" : {
					"properties" : {
						"id" : {
							"type" : "text",
							"fields" : {
								"keyword" : {
									"type" : "keyword",
									"ignore_above" : 256
								}
							}
						},
						"name" : {
							"type" : "text",
							"analyzer": "ngram_analyzer",
							"search_analyzer": "whitespace_analyzer"
						}
					}
				},
				"ocid": {
					"type" : "text",
					"fields" : {
						"keyword" : {
							"type" : "keyword",
							"ignore_above" : 256
						}
					}
				},
				"contractId": {
					"type" : "text",
					"fields" : {
						"keyword" : {
							"type" : "keyword",
							"ignore_above" : 256
						}
					}
				},				
			}
		}
	}

	# Create it again
	result = es.indices.create(index=ES_INDEX, body={"mappings": mappings, "settings": settings}, ignore=[400])

	if 'error' in result and result['error']['reason'] == 'index EDCA already exists':
		print('Updating existing index')
	else:
		pprint(result)

	result = es.indices.create(index=CONTRACT_INDEX, body={"mappings": contract_mapping, "settings": settings}, ignore=[400])

	if 'error' in result and result['error']['reason'] == 'index contract already exists':
		print('Updating existing index')
	else:
		pprint(result)

	result = es.indices.create(index=TRANSACTION_INDEX, body={"mappings": transaction_mapping, "settings": settings}, ignore=[400])

	if 'error' in result and result['error']['reason'] == 'index transaction already exists':
		print('Updating existing index')
	else:
		pprint(result)

	time.sleep(1)

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

			contract_document = {}
			contract_document['_id'] = str(uuid.uuid4())
			contract_document['_index'] = CONTRACT_INDEX
			contract_document['_type'] = 'contract'
			contract_document['_source'] = c
			contract_document['_source']['extra'] = extra

			if 'implementation' in c:
				result = elasticsearch.helpers.bulk(es, transaction_generator(contract_document), raise_on_error=False, request_timeout=120)
				print("transaction", result)

			yield contract_document		

	def generador():
		contador = 0
		# years = ['2017', '2018', '2019']

		for file_name in files:
			print(file_name)

			with open(file_name) as fp:
				for record in ijson.items(fp, 'item'):
					if 'compiledRelease' in record:
						if 'date' in record["compiledRelease"]:
							year = record['compiledRelease']["date"][0:4]
							# print("Year:::::::", year)

							if year:

								document = {}
								document['_id'] = str(uuid.uuid4())
								document['_index'] = ES_INDEX
								document['_type'] = 'record'
								document['doc'] = record
								document['extra'] = extra_fields(record)

								if 'compiledRelease' in record:
									if 'contracts' in record['compiledRelease']:
										result = elasticsearch.helpers.bulk(es, contract_generator(record['compiledRelease']), raise_on_error=False, request_timeout=120)
										print("contract", result)

								yield document
							else:
								pass

	result = elasticsearch.helpers.bulk(es, generador(), raise_on_error=False, request_timeout=120)

	print("record", result)

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

def generarRecordsPorYear(file, year):
	contador = 0
	years = ['2017', '2018', '2019']

	archivos = [] 

	with open(file) as fp:
		for record in ijson.items(fp, 'item'):
			i_year = ''

			file_name = 'todos.json'

			if 'compiledRelease' in record:
				if 'sources' in record['compiledRelease']:
					if len(record['compiledRelease']["sources"]) > 0:
							file_name = record['compiledRelease']["sources"][0]["id"]

				if 'date' in record['compiledRelease']:
					i_year = record['compiledRelease']["date"][0:4]
					file_name += "_" + i_year + ".json"

			# if i_year in years:		
			# 	f = open('archivos_estaticos/records/' + file_name, "a")
			# 	f.write(json.dumps(record))
			# 	f.write(',')
			# 	f.close()

			if file_name in archivos:
				f = open('archivos_estaticos/records/' + file_name, "a")
				f.write(json.dumps(record))
				f.write(',')
				f.close()
			else:
				f = open('archivos_estaticos/records/' + file_name, "a")
				f.write('[')
				f.close()
				archivos.append(file_name)

			if contador == 20:
				break

			contador += 1
			print('contador', contador)

	for a in archivos:
		print('Cerrando archivos', a)
		f = open('archivos_estaticos/records/' + a, "a")
		f.write(']')
		f.close()		

	print('Contador: ', contador)

def generarArchivosEstaticos(file):
	contador = 0

	archivos = [] 

	with open(file) as fp:
		for release in ijson.items(fp, 'item'):
			file_name = 'todos.json'

			if 'sources' in release:
				if len(release["sources"]) > 0:
					file_name = release["sources"][0]["id"]

			if 'date' in release:
				file_name += "_" + release["date"][0:4] + ".json"

			if file_name in Archivos:
				f = open('archivos_estaticos/releases/' + file_name, "a")
				f.write(json.dumps(release))
				f.write(',')
				f.close()
			else:
				f = open('archivos_estaticos/releases/' + file_name, "a")
				f.write('[')
				f.close()
				archivos.append(file_name)

			if contador == 20:
				break

			contador += 1

	for a in archivos:
		f = open('archivos_estaticos/releases/' + a, "a")
		f.write(']')
		f.close()		

	print('Contador: ', contador)

# Importando datos 
startDate = datetime.datetime.now()
print("Fecha y hora inicio de la conversion: ", startDate)


#Generando archivos estaticos

# file_releases = 'archivos_estaticos/pgexport_releases.json'
# generate_json_valid(file_releases, 'releases.json')
# generarArchivosEstaticos('archivos_estaticos/releases.json')

# Fin Generando archivos estaticos
pathArchivo = 'archivos_estaticos/pgexport.json'
generate_json_valid(pathArchivo, 'records.json')

pathElastic = 'archivos_estaticos/records.json'
import_to_elasticsearch([pathElastic,], True)

#Generando records por año: 

# generarRecordsPorYear('archivos_estaticos/records-sefin.json', ['2018','2019','2017'])

#Datos para la db intermedia 
endDate = datetime.datetime.now()
elapsedTime = endDate-startDate
minutes = (elapsedTime.seconds) / 60

print("Fecha y hora fin de la conversion: ", endDate)
print("Tiempo transcurrido: " + str(minutes) + " minutos")
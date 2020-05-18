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

edca_mapping = {
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
		"type": "nested",
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

supplier_mapping = {
  "supplier": {
    "properties": {
      "id": {
        "type": "text",
        "fields": {
          "keyword": {
            "ignore_above": 256,
            "type": "keyword"
          }
        }
      },      
      "name": {
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
      "total_monto_pagado": {
        "type": "float"
      },
      "menor_monto_pagado": {
        "type": "float"
      },
      "mayor_monto_pagado": {
        "type": "float"
      },
      "promedio_monto_pagado": {
        "type": "float"
      },
      "total_monto_contratado": {
        "type": "float"
      },
      "menor_monto_contratado": {
        "type": "float"
      },
      "mayor_monto_contratado": {
        "type": "float"
      },
      "promedio_monto_contratado": {
        "type": "float"
      },    
      "procesos": {
        "type": "long"
      },
      "fecha_ultimo_proceso": {
        "type": "date"
      },
      "publicador": {
        "type": "text",
        "fields": {
          "keyword": {
            "ignore_above": 256,
            "type": "keyword"
          }
        }
      },      
      "procesoImportacionId": {
        "type": "text",
        "fields": {
          "keyword": {
            "ignore_above": 256,
            "type": "keyword"
          }
        }
      }      
    }
  } 
}
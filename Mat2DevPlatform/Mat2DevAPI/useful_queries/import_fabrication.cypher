LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/MaxDreger92/MatGraphAI/master/Mat2DevPlatform/Mat2DevAPI/data/FuelCellFabrication.csv' AS row

MATCH (EMMO_fcas:EMMO_Manufacturing {EMMO__name: "FuelCellAssembly"}),
      (EMMO_meaas:EMMO_Manufacturing {EMMO__name: "CCMManufacturing"})


MERGE(fcfab:Manufacturing {uid: randomUUID(),
run_title: row.`MEA ID`,
DOI: row.DOI,
date_added : "1111-11-11"
})

MERGE(meafab:Manufacturing {uid: randomUUID(),
run_title: row.`MEA ID`,
DOI: row.DOI,
date_added : "1111-11-11"

})
MERGE(EMMO_meaas)<-[:IS_A]-(meafab)<-[:HAS_PART]-(fcfab)-[:IS_A]->(EMMO_fcas)




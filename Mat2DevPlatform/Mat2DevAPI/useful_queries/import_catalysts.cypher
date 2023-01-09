MERGE (cb:Material {
name: "VULCAN XC-72"
})
WITH cb
MATCH(emmo_cb:EMMO_Matter {EMMO__name: "CarbonBlack"})
MERGE(cb)-[:IS_A]->(emmo_cb);


LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/MaxDreger92/MatGraphAI/master/Mat2DevPlatform/Mat2DevAPI/data/Catalysts.csv' AS row
MERGE(cat:Material{name: row.Name,
                    CAS:row.CAS})
WITH cat
MATCH()
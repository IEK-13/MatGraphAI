:auto USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/MaxDreger92/MatGraphAI/master/Mat2DevPlatform/Mat2DevAPI/data/metadata/researchers.csv' AS row
CREATE (institution:Institution{
  ORCID: row.`id`,
  last_name: row.`last_name`,
  first_name: row.first_name,
  date_of_birth: row.date_of_birth,
  date_added: row.date_added,
  field: row.field
  academic_title: row.title
})

MATCH(country:Country {name: row.`country`})
MATCH(country:Country {name: row.`country`})


MERGE(institution)-[:IN]->(country)

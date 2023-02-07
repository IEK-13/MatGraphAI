:auto USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/MaxDreger92/MatGraphAI/master/Mat2DevPlatform/Mat2DevAPI/data/metadata/institutions.csv' AS row
CREATE (institution:Institution{
  ROI: row.`id`,
  name: row.`name`,
  type: row.`types_0`,
  wikipedia_url: row.`wikipedia_url`,
  link: row.`links_0`,
  acronym: row.`acronyms_0`
})

MERGE(country:Country {name: row.`country_country_name`,
                       abbreviation: row.`country_country_code`})

MERGE(institution)-[:IN]->(country)
 
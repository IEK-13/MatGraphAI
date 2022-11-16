CREATE CONSTRAINT n10s_unique_uri ON (r:Resource) ASSERT r.uri IS UNIQUE ;
call n10s.graphconfig.init();
call n10s.onto.import.fetch("https://raw.githubusercontent.com/MaxDreger92/MatGraphAI/master/materials.owl","Turtle")
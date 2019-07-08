CREATE TABLE "mapnik_styles" (
	"LayerName"	TEXT,
	"LayerMinScale"	INTEGER,
	"LayerMaxScale"	INTEGER,
	"StyleName"	INTEGER,
	"StyleFilter"	TEXT,
	"RuleID"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"RuleMinScale"	INTEGER,
	"RuleMaxScale"	INTEGER,
	"RuleFilter"	TEXT,
	"RuleFilterEdit"	TEXT,
	"RuleMarker"	TEXT
);
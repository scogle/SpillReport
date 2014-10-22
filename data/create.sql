CREATE TABLE spills (
	ID	INT PRIMARY KEY		NOT NULL,
	FACID			INT		NOT NULL,
	COMPANY_NAME	TEXT	NOT NULL,
	OPERATOR_NUMBER	INT		NOT NULL,
	DATE			TEXT	NOT NULL,
	LAT				REAL	NOT NULL,
	LONG			REAL	NOT NULL,
	COUNTY			TEXT	NOT NULL
);
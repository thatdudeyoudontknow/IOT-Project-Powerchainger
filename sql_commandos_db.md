CREATE TABLE "HKU" (
	"huisID"	INTEGER NOT NULL,
	"kamerID"	INTEGER NOT NULL,
	"userID"	INTEGER NOT NULL,
	PRIMARY KEY("huisID","kamerID","userID"),
	FOREIGN KEY("huisID") REFERENCES "huis"("huisID"),
	FOREIGN KEY("kamerID") REFERENCES "kamer"("kamerID"),
	FOREIGN KEY("userID") REFERENCES "user"("userID")
);

CREATE TABLE "huis" (
	"huisID"	INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	"huisnaam"	TEXT NOT NULL,
	"verbruik_per_huis"	REAL
);

CREATE TABLE "kamer" (
	"huisID"	INTEGER NOT NULL,
	"kamerID"	INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	"kamernaam" TEXT NOT NULL,
	FOREIGN KEY("huisID") REFERENCES "huis"("huisID")
);


CREATE TABLE "user" (
	"userID"	INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	"gebruikersnaam"	TEXT NOT NULL,
	"wachtwoord"	TEXT NOT NULL,
	"email"	TEXT NOT NULL
);

CREATE TABLE "vrienden" (
	"userID"	INTEGER NOT NULL,
	"vriendenID"	INTEGER NOT NULL,
	PRIMARY KEY("vriendenID","userID"),
	FOREIGN KEY("userID") REFERENCES "user"("userID"),
	FOREIGN KEY("vriendenID") REFERENCES "user"("userID")
);

CREATE TABLE "verbruik" (
	"huisID"	INTEGER NOT NULL,
	"kamerID"	INTEGER NOT NULL,
	"userID"	INTEGER NOT NULL,
	"verbruik"	REAL,
	"datetime"	TEXT NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', '+02:00')),
	PRIMARY KEY("huisID", "kamerID", "userID", "datetime"),
	FOREIGN KEY("huisID") REFERENCES "huis"("huisID"),
	FOREIGN KEY("kamerID") REFERENCES "kamer"("kamerID")
	FOREIGN KEY("userID") REFERENCES "user"("userID")
);

INSERT INTO "huis" ("huisnaam") VALUES ('van doornveste');
INSERT INTO "kamer" ("huisID", "kamernaam") VALUES (1,'woonkamer');
INSERT INTO "user" ("gebruikersnaam", "wachtwoord","email") VALUES ('Flapoor','Welkom123', 'test@test.nl');
INSERT INTO "HKU" ("huisID", "kamerID", "userID") VALUES (1,1,1);

INSERT INTO "huis" ("huisnaam") VALUES ('giethoorns');
INSERT INTO "kamer" ("huisID", "kamernaam") VALUES (2,'Woonkamer');
INSERT INTO "user" ("gebruikersnaam", "wachtwoord","email") VALUES ('Admin','Welkom123', 'tessst@test.nl');
INSERT INTO "HKU" ("huisID", "kamerID", "userID") VALUES (2,2,2);

INSERT INTO "huis" ("huisnaam") VALUES ('liefmans');
INSERT INTO "kamer" ("huisID", "kamernaam") VALUES (3,'19');
INSERT INTO "user" ("gebruikersnaam", "wachtwoord","email") VALUES ('Henk','Welkom123', 'tegst@test.nl');
INSERT INTO "HKU" ("huisID", "kamerID", "userID") VALUES (3,3,3);

INSERT INTO "huis" ("huisnaam") VALUES ('applebandit');
INSERT INTO "kamer" ("huisID", "kamernaam") VALUES (4,'31B');
INSERT INTO "user" ("gebruikersnaam", "wachtwoord","email") VALUES ('Waldo','Welkom123', 'teassst@test.nl');
INSERT INTO "HKU" ("huisID", "kamerID", "userID") VALUES (4,4,4);

drop table HKU;
drop table huis;
drop table kamer;
drop table user;
drop table vrienden;
drop table verbruik;



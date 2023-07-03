CREATE TABLE "HKU" (
    "huisID" INTEGER PRIMARY KEY,
    "kamerID" INTEGER,
    "userId" INTEGER
);

CREATE TABLE "huis" (
    "huisID" INTEGER PRIMARY KEY AUTOINCREMENT,
    "userID" INTEGER,
    "huisnaam" TEXT,
    "woonplaats" TEXT NOT NULL,
    "huisnummer" INTEGER NOT NULL,
    "toevoeging" TEXT,
    "straat" TEXT NOT NULL,
    "postcode" TEXT NOT NULL
);

CREATE TABLE "kamer" (
    "kamerID" INTEGER PRIMARY KEY AUTOINCREMENT,
    "kamernaam" TEXT NOT NULL,
    "huisnummer" INTEGER NOT NULL,
    "userID" INTEGER
);


CREATE TABLE "user" (
    "id" INTEGER PRIMARY KEY,
    "email" TEXT NOT NULL UNIQUE,
    "username" TEXT NOT NULL UNIQUE,
    "password_hash" TEXT NOT NULL
);

CREATE TABLE "vrienden" (
    "userID" INTEGER,
    "vriendenID" INTEGER,
    PRIMARY KEY ("vriendenID", "userID"),
    FOREIGN KEY ("userID") REFERENCES "user" ("id"),
    FOREIGN KEY ("vriendenID") REFERENCES "user" ("id")
);

CREATE TABLE "verzoeken" (
    "verzoekID" INTEGER PRIMARY KEY AUTOINCREMENT,
    "userID" INTEGER NOT NULL,
    "vriendenID" INTEGER NOT NULL,
    "status" TEXT,
    FOREIGN KEY ("userID") REFERENCES "user" ("id"),
    FOREIGN KEY ("vriendenID") REFERENCES "user" ("id")
);

CREATE TABLE "verbruik" (
    "verbruikID" INTEGER PRIMARY KEY AUTOINCREMENT,
    "huisID" INTEGER,
    "kamerID" INTEGER,
    "userID" INTEGER,
    "verbruik" REAL,
	"datetime" DATETIME DEFAULT (DATETIME('now', '+2 hours')),
    UNIQUE ("verbruikID","huisID", "kamerID", "userId")
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
drop table verzoeken;



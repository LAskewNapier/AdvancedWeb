Drop table IF EXISTS Users;

CREATE TABLE Users(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);

DROP table IF EXISTS Creatures;

CREATE TABLE Creatures(
    Creature_id INTEGER PRIMARY KEY AUTOINCREMENT,
    cName TEXT,
    HP TEXT,
    type TEXT,
    STR TEXT,
    DEX TEXT,
    CON TEXT,
    cINT TEXT,
    WIS TEXT,
    CHA TEXT,
    PB TEXT,
    AC TEXT,
    THROW TEXT,
    SIZE TEXT,
    HDICE TEXT
);

DROP TABLE IF EXISTS UsersCreations;

CREATE TABLE UsersCreations(
    user_id INTEGER,
    Creature_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES Users (user_id),
    FOREIGN KEY (Creature_id) REFERENCES Creatures (Creature_id)
)

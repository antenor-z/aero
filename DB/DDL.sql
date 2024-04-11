CREATE TABLE Aerodrome (
    ICAO VARCHAR(4) PRIMARY KEY,
    AerodromeName VARCHAR(100) NOT NULL,
    City VARCHAR(100) NOT NULL,
    Latitude DECIMAL(9, 6) NOT NULL,
    Longitude DECIMAL(9, 6) NOT NULL,
    UNIQUE (AerodromeName)
);

CREATE TABLE PavementType (
    Code VARCHAR(3) PRIMARY KEY,
    Material VARCHAR(50) NOT NULL
);

CREATE TABLE Runway (
    ICAO VARCHAR(4) NOT NULL,
    Head1 VARCHAR(3) NOT NULL,
    Head2 VARCHAR(3) NOT NULL,
    RunwayLength INT(4),
    RunwayWidth INT(2),
    PavementCode VARCHAR(3),
    PRIMARY KEY (ICAO, Head1),
    FOREIGN KEY (ICAO) REFERENCES Aerodrome (ICAO),
    FOREIGN KEY (PavementCode) REFERENCES PavementType (Code),
    UNIQUE (ICAO, Head1, Head2)
);

CREATE TABLE CommunicationType (
    CommType VARCHAR(20) PRIMARY KEY
);

CREATE TABLE Communication (
    Id INT AUTO_INCREMENT,
    ICAO VARCHAR(4),
    Frequency DECIMAL(6, 3) NOT NULL,
    CommType VARCHAR(20),
    PRIMARY KEY (ICAO, Id),
    FOREIGN KEY (ICAO) REFERENCES Aerodrome (ICAO),
    FOREIGN KEY (CommType) REFERENCES CommunicationType (CommType),
    UNIQUE (ICAO, Frequency)
);

CREATE TABLE ILSCategory (
    Category VARCHAR(10) PRIMARY KEY
);

CREATE TABLE ILS (
    ICAO VARCHAR(4),
    Ident VARCHAR(20) NOT NULL,
    Frequency DECIMAL(6, 3) NOT NULL,
    Category VARCHAR(10) NOT NULL,
    CRS VARCHAR(10) NOT NULL,
    Minimum INT,
    PRIMARY KEY (ICAO, Ident),
    FOREIGN KEY (ICAO) REFERENCES Aerodrome (ICAO),
    FOREIGN KEY (Category) REFERENCES ILSCategory (Category),
    UNIQUE (ICAO, Frequency),
    UNIQUE (ICAO, Ident)
);

CREATE TABLE VORNDB (
    ICAO VARCHAR(4),
    Ident VARCHAR(20) NOT NULL,
    Frequency DECIMAL(6, 3) NOT NULL,
    PRIMARY KEY (ICAO, Ident),
    FOREIGN KEY (ICAO) REFERENCES Aerodrome (ICAO),
    UNIQUE (ICAO, Frequency)
);
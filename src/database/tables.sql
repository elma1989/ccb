CREATE TABLE country(
    cty_cs VARCHAR(3) NOT NULL PRIMARY KEY,
    cty_name VARCHAR(20) NOT NULL
);
CREATE TABLE ingrediant(
    igdt_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    igdt_name VARCHAR(30) NOT NULL UNIQUE
);
CREATE TABLE recepe(
    rcp_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    rcp_name VARCHAR(30) NOT NULL,
    rcp_preparation TEXT,
    cty_cs VARCHAR(3) NOT NULL REFERENCES country(cty_cs) ON DELETE CASCADE
);
CREATE TABLE recepe_ingrediant(
    rcp_id INTEGER NOT NULL REFERENCES recepe(rcp_id) ON DELETE CASCADE,
    igdt_id INTEGER NOT NULL REFERENCES ingrediant(igdt_id),
    igdt_anmount DECIMAL(5.2) NOT NULL,
    igdt_unit VARCHAR(3) NOT NULL
);
use mapping_system;

CREATE TABLE users (
  id CHAR(36) NOT NULL DEFAULT (REPLACE(UUID(),'-','')),
  username VARCHAR(255) NOT NULL UNIQUE,
  firstname VARCHAR(255) NOT NULL,
  lastname VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL,
  PRIMARY KEY (id)
);
CREATE TABLE Mappings(
    id CHAR(36) NOT NULL,
    user_id CHAR(36) NOT NULL,
    username VARCHAR(255),
    Commt VARCHAR(255),
    Editdate DATETIME,
    Status VARCHAR(255),
    PRIMARY KEY (id),
    CONSTRAINT FOREIGN KEY (user_id) REFERENCES users(id)
);
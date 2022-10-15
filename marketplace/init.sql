CREATE USER porstgres_user with encrypted password 'qwerty123';
CREATE DATABASE marketplace;
GRANT ALL PRIVILEGES ON DATABASE marketplace TO porstgres_user;
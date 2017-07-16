CREATE USER whatsinmyfridge;
ALTER USER whatsinmyfridge WITH PASSWORD 'Cr33d3nc3';
ALTER USER whatsinmyfridge CREATEDB;
CREATE DATABASE whatsinmyfridge OWNER whatsinmyfridge;
GRANT ALL PRIVILEGES ON DATABASE whatsinmyfridge TO whatsinmyfridge;
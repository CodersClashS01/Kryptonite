CREATE USER 'codeclash'@'localhost' IDENTIFIED BY 'codeclash';
CREATE DATABASE codeclash;
GRANT ALL PRIVILEGES ON codeclash.* TO 'codeclash'@'localhost';
FLUSH PRIVILEGES;

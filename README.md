# Refactoring Star Trek Chronology Table
A little Sunday afternoon project.  
I've been watching Star Trek in chronological order but was struggling to follow the simple HTML table I found, so I scraped and rebuilt it.  
Episode list pulled from https://www.johnstonsarchive.net/startrek/st-episodes-1.html

### What it does
First it scrapes the original website, placing the HTML table into a python list  
Next it inserts the list into a postgres database
Finaly... well, that's all it does for now

### Postgres database
Create database on Ubuntu
> sudo -u postgres psql
> CREATE DATABASE startrekdb;
> CREATE USER [username] WITH ENCRYPTED PASSWORD [password];
> GRANT ALL ON DATABASE startrekdb TO [username];
Then set DB_USERNAME and DB_PASSWORD in your OS environment variables to match the above


### Future Additions
- Use context manager for postgres connection
- Turn into Flask app
- Add original air dates
- Add sorting and filtering features
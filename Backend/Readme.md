Software's to install:
Pg Admin4 for Database -postgres
https://www.enterprisedb.com/downloads/postgres-postgresql-downloads

** Make sure u set the password as 12345 for the database **

Once Pg Admin has been installed, open the Server Tab on the left side, Once u are in the DataBase Section, u will find a postgres default database, create a database called progsd

After the progsd Database has been created, go into the directory where the requirements.txt is present and use:
                pip install -r requirements.txt

Once the requirements have been installed,
Use command:    python manage.py migrate

This will migrate all the databases to the created table progsd

After migrations are completed,

Use command :     python manage.py runserver

When u get a display like:
\
System check identified no issues (0 silenced).
October 31, 2022 - 15:56:26
Django version 4.1.1, using settings 'progsd.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.

The server is working and U can go ahead with the application
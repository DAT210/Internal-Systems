# Internal Systems &middot; [![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](https://github.com/your/your-project/blob/master/LICENSE)
> Administrative functions and systems used by employees

Developed by Group 4 along with Menu and Food Preparation. Links to the other repositories: 

https://github.com/DAT210/Menu
https://github.com/DAT210/Food-Preparation

## Setting up with Docker

Clone the repository and navigate to the `Internal-Systems` folder in a terminal that supports Docker. Then use `docker-compose` to run the containers:

```shell
cd <your_path>/Internal-Systems
docker-compose up --build
```

Then you can should be able to access the menu database admin webpage in your browser at http://localhost

## Running the app without Docker

Clone the repository and go to the `Internal-Systems/src/Admin Menu Database` folder. From here you can run `app.py`.

To use the database you have to run the sql-script `Internal-Systems/src/Admin Menu Database/init_menu_db.sql` in MySQL and then setup a MySQL server on the machine. Furthermore you have to change the `user_info["username"]` parameter in `Internal-Systems/src/Admin Menu Database/app.py` from `mysql` to `localhost`.

Then you can should be able to access the menu database admin webpage in your browser at http://localhost

## Developing

### Built With
The menu database admin webpage is built with the Flask framework in Python, HTML-templating with Jinja and JavaScript/jQuery. It also uses Bootstrap for styling.

### Prerequisites
If you run the code by using Docker you need a working installation of Docker. If you wish to run it without installing Docker you need Python, MySQL and MySQL server.

https://docs.docker.com/install/


## Database

We use the latest version of MySQL. Dependencies are automatically downloaded when using Docker.


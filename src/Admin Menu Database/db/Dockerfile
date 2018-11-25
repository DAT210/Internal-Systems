FROM mysql/mysql-server:latest
COPY ["init_menu_db.sql", "/docker-entrypoint-initdb.d/"]
ENV MYSQL_ROOT_PASSWORD=root
EXPOSE 3306

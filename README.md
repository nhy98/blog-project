
## Install Instruction
Modify database connection string in /src/config/config.yaml file.
Restore database from sql file placed in /src/config/data.sql.

```
sudo apt-get update
sudo apt-get install mysql-client
mysql -h [host] -P [port] -u [user] -p [database_name] < [filename].sql
```

The demo app can be run as following:

```
pip -r install requirements.txt
python app.py
```

The examples and demo app can also be built and run as a Docker image/container:

```
docker build -t blogproject .
docker run -p 5000:5000 --name blogproject blogproject
```


> NOTE: Access API swagger (http://localhost:5000/apidocs/)

# API Specification

1. Users
- /user/login [GET] : Login by Facebook or Google account.
- /user/ [GET]: Get information of a user.
- /user/all [GET]: Get all user in the system.
- /user/ [PUT]: Update user information.
2. Blog Post
- /post/ [GET]: Get blog post by post id.
- /post/all [GET]: Get blog posts of all users in the system.
- /post/ [POST]: Create a blog post.
- /post/ [PUT]: Update blog post.
- /post/ [DELETE]: Delete a blog post.
3. Interaction for Blog Post
- /interaction/ [GET]: Get interaction of a post.
- /interaction/ [POST]: Create an interaction by post id.
- /interaction/ [DELETE]: Delete interaction.

Test Facebook Account: 
1. New register: mkgtebolse_1628913022@tfbnw.net - psw: 1-8@Abc	
2. Old account: taxldldpza_1628913022@tfbnw.net	 - psw: 1-8@Abc
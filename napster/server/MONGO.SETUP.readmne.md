#How to Setup MongoDB

##1: Get MongoDB
> MongoDB is a scalable, high-performance, open source NoSQL database. 

Install Mongo on your system, follow the [instructions](http://www.mongodb.org/display/DOCS/Quickstart) on MongoDB website

[MongoDB API by Tutorials](http://www.mongodb.org/display/DOCS/Tutorial)

##2: Setup MongoEngine
>MongoEngine is an Object-Document Mapper, written in Python for working with MongoDB

To install run ` pip install mongoengine`. More detailed info can be found [here](http://mongoengine.org/docs/v0.4/index.html) 

[MongoEngine API](http://mongoengine.org/docs/v0.4/apireference.html)

##3: Start everything
Simply open a terminal and go in your MongoDB root folder, then launc your local server with the command `./bin/mongod`

Piece of cake ;)

If you want to check your Mongo database to see if the data are present just run a mongo console in a terminal with the command `./bin/mongo` and use:

* `use Napster` to connect with the database named Napster
* `db.user.find()` to see all the documents in the <strong>user</strong> collection
*  `db.file.find()` to see all the documents in the <strong>file</strong> collection

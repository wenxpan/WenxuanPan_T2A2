# T2A2 - Cat Diet API

## Links

- [Github repo](https://github.com/wenxuan-pan/WenxuanPan_T2A2)
- [Trello Board](https://trello.com/b/IJJ0hY8f/t2a2-implementation-plan)
- [API Documentation](https://documenter.getpostman.com/view/28027782/2s93zB5MTY)

## Installation and setup

- Open terminal and run the PostgreSQL prompt:

```
psql
```

- Create and connect to database

```
Create DATABASE cat_diet;
\c cat_diet;
```

- Create a user with password and grant user priviliges:

```
CREATE USER cat_diet_dev WITH PASSWORD 'admin123';
GRANT ALL PRIVILEGES ON DATABASE cat_diet TO cat_diet_dev;
```

- Open another terminal. Use `cd` command and direct to the `WenxuanPan_T2A2/src` directory

- Create and activate virtual environment

```
python3 -m venv .venv
source .venv/bin/activate
```

- Install dependencies

```
python3 -m pip install -r requirements.txt
```

- Rename `.env.sample` to `.env`, and set the db connection string and JWT secret key:

```
DB_URI=postgresql+psycopg2://cat_diet_dev:admin123@localhost:5432/cat_diet
JWT_SECRET_KEY=Your Secret Key
```

- In terminal, create and seed the database, then run the flask app:

```
flask db create
flask db seed
flask run
```

The server will run on `http://127.0.0.1:5000`.

## Problem identification and justification (R1/R2)

The REST Cat Diet API aims to assist cat owners in tracking and managing their cat's diet and food preferences, as well as monitoring any changes over time, in order to keep a well-balanced diet for their cats.

In particular, the app addresses the following issues:

- **Fussy eating:** Many cats are known to be picky eaters, and it can be challenging for cat owners to identify their cat's favourite and least favourite foods. The app provides a centralised platform for cat owners to record and track their cat's preferences, making it easier for them to choose suitable food options.

- **Health and nutrition**: The [Code of Practice for the Private Keeping of Cats](https://agriculture.vic.gov.au/livestock-and-animals/animal-welfare-victoria/domestic-animals-act/codes-of-practice/code-of-practice-for-the-private-keeping-of-cats#h2-6) sets the following minimum standards regarding nutrition:

  > Cats must be fed a diet that provides proper and sufficient food to maintain good health and meet their physiological needs.
  >
  > Cats are carnivores and must not be fed a purely vegetarian diet.
  >
  > Cats must not be fed a diet consisting purely of fresh meat (including fish).

  To meet these standards, owners can use this app to regularly monitor the food type and ingredients to ensure that their cat receives the necessary nutrients and avoid potential health issues caused by an imbalanced diet.

- **Avoiding overfeeding treats:** Treats are given as rewards for cats, but excessive consumption can lead to weight gain and health issues, and owners might not always realise that they are overfeeding. The app allows cat owners to keep track of treat consumption and review on a regular basis to prevent overfeeding.

- **Identifying allergies or intolerances:** Cats can have allergies or food intolerances, and it may take time for owners to realised and identify specific ingredients or brands that cause adverse reactions in their cats. The app allows users to note down their cat's any resistance or adverse reactions to certain foods or ingredients, which can be helpful during vet consultation and finding solutions. This will also help cat owners remember and avoid purchasing similar products in the future.

## Database system: benefits and drawbacks (R3)

I have chosen PostgreSQL as the database management system, because of the following benefits:

- It is a free and open source database management system.
- It is good at handling large datasets effectively. It is ACID (Atomicity, Consistency, Isolation, Durability)compliant, which means it ensures the reliability and consistency of the stored data. This helps as the app will be potentially tracking and managing a large number of users, cats, foods, ingredients, and notes. The ability to maintain data integrity and handle complex relationships makes PostgreSQL a suitable choice.
- It is a relational database, which provides a more structured and organized approach to store and manage data than a non-relational database. This structure aligns well with the entities in the app. The relational model allows for clear definition of entities and relationships between them, making it easier to establish and maintain data consistency.
- PostgreSQL has an active community of developers and users and provides accessible documentation and support. Additionally, PostgreSQL integrates well with various programming languages and frameworks, including Python and Flask for this project using SQLAlchemy as the ORM.

There are some drawbacks to be considered:

- As a relational database system, it may have limitations when it comes to storing data with varying structures. Adding new attributes to a record often requires adding a new column to the entire table, which can be less flexible compared to non-relational databases. This drawback might be avoided with careful planning and design, ensuring that the schema reflects all the needed functionalities of the app, instead of users needing to add custom properties later on.
- Data stored in PostgreSQL is not straightly compatible with objects in a programming language. This is different to a non-relational database which the data objects are usually in JSON format and can be stored directly in it. In this project, the issue is solved using marshmallow, a serialisation and deserialisation tool that helps convert data to formatted JSON result; it also has the adds-on benefit to validate and sanitize input data.
- In terms of reading performance, PostgreSQL might not be as good as other systems such as MySQL. This is because it creates a new system process for each user connected to the database, [allocating a significant amount of memory (approximately 10 MB)](https://aws.amazon.com/compare/the-difference-between-mysql-vs-postgresql) for each connection, whereas MySQL utilizes a single process to handle multiple users, resulting in better performance for applications that primarily involve reading and displaying data to users. However, considering that PostgreSQL still performs better in frequent data updates and concurrent write operations, it remains a suitable option for this project.

Overall, PostgreSQL is well-suited for the content and requirements of the app. It effectively manages the relationships between various entities including users, cats, foods, ingredients, and notes. The relational database structure allows for clear definition of these entities and their relationships, enabling efficient querying and retrieval of related data. For example, the relationships between cats and their owners (users) can be easily established and tracked using foreign key constraints. The ability to store and retrieve complex relationships between entities makes PostgreSQL a suitable choice for this app's content despite its limitations.

## Functionalities and benefits of an ORM (R4)

An Object Relational Mapper (ORM) plays a crucial role in connecting object-oriented programming (OOP) with relational databases. It offers several key functionalities and benefits, which are particularly relevant to the Cat Diet API project:

- Using SQLAlchemy as the ORM, the developer can interact the database using python instead of writing SQL queries directly. For example, writing `db.select(Cat)` in python will be converted by ORM to SQL query like `SELECT * FROM cats`. It helps abstracts away the complexities of SQL syntax to let developers [focus on high-level implementation](https://www.educative.io/answers/what-is-object-relational-mapping).
- Using ORM can generate objects that map to database tables, providing an object-oriented approach to data manipulation. In this project, each entity (users, cats, foods etc.) corresponds to a model class, and the attributes of each class represent the fields of the tables.

Example - User model defined using SQLAlchemy:

```python
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    joined_since = db.Column(db.Date, default=date.today())

    cats = db.relationship('Cat', back_populates='owner',
                           cascade='all, delete')
```

users table generated in PostgreSQL:
![users table](/docs/table-postgres.png)

- ORM supports mapping relationships between classes/models to relationships between database tables using foreign keys. This feature is valuable for establishing relationships between entities in the app, such as the relationship between users and cats or between foods and ingredients. The ORM simplifies the management of these relationships and enables cascade behavior when performing operations on related objects.
- SQLAlchemy provides [session management](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#what-does-the-session-do), which acts as a container for maintaining conversations with the database. The session holds the ORM objects affected by the transaction and ensures that they are committed to the database together or not at all (using `session.commit()`). This is useful for maintaining consistency and integrity of the data.

## API endpoints (R5)

Here is an overview of the API endpoints:
![endpoints-overview](docs/endpoints-overview.png)

Visit links below to see full documentation:

- [API documentation - Postman version](https://documenter.getpostman.com/view/28027782/2s93zB5MTY#intro)
- [API documentation - Markdown version](/docs/endpoints.md)

## ERD and database relations (R6/R9)

### ERD

![ERD for Cat Diet API](./docs/erd.png)

<!-- R9 (database terminology) - at the lower level, the same relationships at the database level; tables, foreign key, primary key, use database language to talk about how it works, how the relationships work -->

### Table - users

This table stores essential information about the user.

Attributes:

- id: auto-generated integer, primary key of the table
- username: name to be displayed in the user profile (does not need to be real name), the string is mandatory, should be unique and not exceed 15 characters
- password: password of the user's account which cannot be set null
- is_admin: a boolean showing whether the user has admin rights which cannot be set null
- joined_since: the date user registers the account; it is auto generated and cannot be changed by users

Relationships:

- one-to-many relationship between users and cats: A user can have many or no cats, a cat can only belong to one user

### Table - cats

This table stores information about the cats owned by the users.

Attributes:

- id: auto-generated integer, primary key of the table
- name: name of the cat, the string is mandatory and should be no longer than 100 characters. There can be duplicate names for cats.
- year_born: the year that the cat was born. It should be integer and can be set null.
- year_adopted: the year that the cat was adopted by the user. It should be integer and can be set null. It should not be earlier than year_born.
- breed: breed of the cat, it should be a string no longer than 100 characters.
- owner_id: this is a foreign key and references to id in users table. It represents the one-to-many relationship between cats and users. It cannot be set to null - a cat must have a owner.

Relationships:

- one-to-many relationship between users and cats: A user can have many or no cats, a cat can only and must belong to one user. The cat will be deleted if their owner gets removed.
- one-to-many relationship between cats and notes: There can be many or no notes about a cat, and a note should only and must be about one cat.

### Table - notes

This table stores information about the notes created by the user to track their cat's reaction to foods.

Attributes:

- id: auto-generated integer, primary key of the table
- message: a string representing content of the note
- rating: an integer (-1, 0, or 1), indicating whether the note is negative, neutral or positive
- date_recorded: the date recorded in the note
- cat_id: a foreign key that references id in the cats table. It represents the one-to-many relationship between notes and cats
- food_id: a foreign key that references id in the foods table. It represents the one-to-many relationship between notes and foods

Relationships:

- one-to-many relationship between notes and cats: There can be many or no notes about a cat, and a note should only and must be about one cat. The note will be deleted if the cat gets deleted.
- one-to-many relationship between notes and foods: There can be many or no notes about a food, and a note should only and must be about one food. The note will be deleted if the food gets deleted
- It does not have an explicit relationship with users, because it can be deduced from its relationship with the cat (e.g. note.cat.owner_id); only the cat owner can take notes about their cats.

### Table - foods

This table stores information about the cat foods.

Attributes:

- id: auto-generated integer, primary key of the table
- name: a string that represents the name of the food, it should not exceed 200 characters and should be mandatory and unique
- brand: the brand of the food (can be set to null), a string not exceeding 100 characters
- category: the type that the food belongs to, it should be one of: 'Wet', 'Dry', 'Freeze-dried', 'Raw', 'Cooked', 'Treats'

Relationships:

- One-to-many relationship between notes and foods: There can be many or no notes about a food, and a note should only and must be about one food.
- Many-to-many relationship between foods and ingredients: A food can contain many or no ingredients, and an ingredient can be included in many or no foods. This is reflected in the join table food_ingredients.

### Table - ingredients

This table stores information about the ingredients that can be contained in foods.

Attributes:

- id: auto-generated integer, primary key of the table
- name: a string that represents the name of the ingredient, it should not exceed 100 characters and should be mandatory and unique
- category: the type that the ingredient belongs to, it should be one of: 'Meat', 'Seafood', 'Derivatives', 'Grains', 'Vegetables', 'Other'

Relationships:

- Many-to-many relationship between foods and ingredients: A food can contain many or no ingredients, and an ingredient can be included in many or no foods. This is reflected in the join table food_ingredients below.

### Join table - food_ingredients

Attributes

- food_id: this is a foreign key that references id in the foods table. It is an integer and should not be set null
- ingredient_id: this is a foreign key that references id in the ingredients table. It is an integer and should not be set null. Together with food_id, the two attributes form primary keys of this table.

## Third party services (R7)

The REST API was built using Flask, a Python micro-framework that runs on the server-side, providing essential functionalities to handle the incoming request, determine the route and request methods, and send an appropriate response back to the client.

Flask itself is lightweight and has a flexible structure, and various packages can be added to the app to achieve additional functionalities.

The following third-party services are used in this app (for full list, see [src/requirements.txt](/src/requirements.txt)).

### SQLAlchemy (2.0.16) & Flask-SQLAlchemy (3.0.3)

SQLAlchemy is an ORM tool that serves as a bridge between python and the database (postgreSQL). In this project, it is used together with its wrapper Flask-SQLAlchemy to define models that represent database tables using python classes as well as translating python codes into SQL queries, achieving an object-oriented approach to data manipulation and makes the code easier to maintain.

Example usage of SQLAlchemy:

```python
# in init.py, create the db object using flask-sqlalchemy
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# in app.py, configure PostgreSQL database, initialise the app with the extension
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URI')
db.init_app(app)

# in user.py, define the User model
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

# in cli_bp.py, create user table, seed table with existing data
db.create_all()
db.session.add_all(users)
db.session.commit()

# in auth_bp.py, query table data
stmt = db.select(User).filter_by(email=request.json['email'])
user = db.session.scalar(stmt)
```

### psycopg2 (2.9.6)

Psycopg is the [PostgreSQL database adapter](https://pypi.org/project/psycopg2/) for Python. It is specified in the DB_URI connection string, e.g. `DB_URI="postgresql+psycopg2://dev:password@localhost:5432/db"`, in order to assist SQLAlchemy to interact with PostgreSQL.

### marshmallow (3.19.0) & Flask-marshmallow (0.15.0)

Marshmallow is an ORM library used to:

- convert app-level objects to JSON format using `Schema.dump()`
- load input data to app-level objects using `Schema.load()`
  - raise `ValidationError` when input data doesn't meet validation requirements

Example usage of marshmallow:

```python
# in init.py, create the ma object using flask-marshmallow
from flask_marshmallow import Marshmallow
ma = Marshmallow()

# in app.py, initialise the app with the extension
ma.init_app(app)

# in user.py, define user schema
class UserSchema(ma.Schema):
    # specify validation requirements
    email = fields.Email(required=True)
    is_admin = fields.Boolean(load_default=False)
    class Meta:
        fields = ('id', 'username', 'email', 'password',
                  'is_admin', 'joined_since', 'cats')

# in users_bp.py, convert ORM object to JSON result
UserSchema(exclude=['password', 'cats']).dump(user)

# in users_bp.py, convert JSON result to ORM object as well as sanitising input
user_info = UserSchema().load(request.json, partial=True)
```

### Flask-Bcrypt (1.0.1)

Flask-Bcrypt is a Flask extension that provides bcrypt hashing utilities for application. It is designed to be ["de-optimized"](https://pypi.org/project/Flask-Bcrypt/) so that hashed data is more difficult to crack than other faster algorithms.

In this project, it is used to hash user passwords before storing it to db and verify passwords during login. By doing so, it adds an additional security layer and ensures that sensitive data is safely handled and will not expose to anyone.

Example usage of flask-bcrypt:

```python
# in init.py, create bcrypt object
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

# in app.py, initiate app with the extension
bcrypt.init_app(app)

# in auth_bp.py, hash the password before creating model instance
password=bcrypt.generate_password_hash(
            user_info['password']).decode('utf-8')

# check the input password against hashed password stored in db
bcrypt.check_password_hash(user.password, request.json['password'])
```

Hashed passwords are stored in postgresql database, so even admin is not able to access raw passwords:
![Hashed password in database](/docs/hashed-password.png)

### python-dotenv (1.0.0)

Python-dotenv is used to read key-value pairs from a .env file and can set them as environment variables.

In this project, `.env` file is created to store JWT secret key and SQLAlechemy's database connection string. The file is not published to remote repo, ensuring that confidential information is stored safely, and users can set their own environment variables on their end by setting up `.env` file.

```python
# in app.py, import environment variables
from os import environ
app.config['JWT_SECRET_KEY'] = environ.get('JWT_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URI')
```

### Flask-JWT-Extended (4.5.2)

Flask-JWT-Extended is used to integrate JWT (JSON Web Tokens) support in the flask app. This helps to ensure that user's identity is authenticated before they perform sensitive operations. For example, a person cannot create new food if they are not logged in (i.e. no token in the request header). It also helps maintaining authorisation levels. For example, a user cannot add notes for a cat that they don't own; this is verified by getting identity from the token and checking it against the owner id in the database.

Example usage of flask-jwt-extended:

```python
# in init.py, create jwt object
from flask_jwt_extended import JWTManager
jwt = JWTManager()

# in app.py, initiate app with extension
jwt.init_app(app)

# in auth_bp.py, jwt token is generated with user id after verification
from flask_jwt_extended import create_access_token
token = create_access_token(
                identity=user.id, expires_delta=timedelta(days=1))

# in blueprints, jwt_required() decorator is used to protect routes
@jwt_required()

# in utils.authorise, get_jwt_identity is used to determine token identity
user_id = get_jwt_identity()
```

User token is returned when logged in:
![Response token](/docs/response-token.png)

If user does not add bearer token in the request header for protected routes, it will return 401 error with the message:

```JSON
{
    "msg": "Missing Authorization Header"
}
```

Or if the token identity does not match the authorisation level, it will return message like this:

```JSON
{
    "error": "401 Unauthorized: You must be an admin"
}
```

## Porject models and relationships (R8)

Describe your projects models in terms of the relationships they have with each other

<!-- R8 (python code) - about SQLAlchemy models, relationships between the models using sqlalchemy language; `db.relationship`, `db.ForeignKey` -->

There are 5 models created in this project: User, Cat, Food, Ingredient, Note. There is an additional join table food_ingredient that reflects the many-to-many relationship between Food and Ingredient.

### User model

```python
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    joined_since = db.Column(db.Date, default=date.today())

    cats = db.relationship('Cat', back_populates='owner',
                           cascade='all, delete')
```

- The primary key of the model is `id`, defined using `primary_key=True`.
- `username`, `email`, `password` and `is_admin` are set as `nullable=False`, meaning they are required fields. If no value of `is_admin` is given, it will be set as default False.
- Instead of `db.ForeignKey`, the User model just has a `db.relationship` with `cats`, representing the one-to-many relationship: one user can have many cats; and as it back populates with the single `owner` in `Cat` model, one cat can only belong to one owner. `cascade='all, delete'` means that the cats will be removed if their owner is deleted.

Returned JSON result:

```JSON
{
    "id": 2,
    "username": "John",
    "email": "john@gmail.com",
    "is_admin": false,
    "joined_since": "2023-06-20",
    "cats": [
        {
            "id": 1,
            "name": "Luna",
            "breed": "Domestic Shorthair",
            "year_born": 2020,
            "year_adopted": 2021
        }
    ]
}
```

The nested list of cats is created through marshmallow schema:

```python
cats = fields.List(fields.Nested('CatSchema', exclude=['owner_id', 'owner', 'notes']))
```

### Cat model

```python
class Cat(db.Model):
    __tablename__ = 'cats'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    year_born = db.Column(db.Integer)
    year_adopted = db.Column(db.Integer)
    breed = db.Column(db.String(100))

    owner_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    owner = db.relationship('User', back_populates='cats')

    notes = db.relationship(
        'Note', back_populates='cat', cascade='all, delete')
```

returned JSON result

```JSON
{
    "id": 1,
    "name": "Luna",
    "breed": "Domestic Shorthair",
    "year_born": 2020,
    "year_adopted": 2021,
    "owner": {
        "username": "John"
    },
    "notes": []
}
```

marshmallow schema

```python
owner = fields.Nested('UserSchema', only=[
                      'username'])
notes = fields.List(fields.Nested('NoteSchema', exclude=[
    'cat', 'cat_id', 'food_id']))
```

### Food model

```python
class Food(db.Model):
    __tablename__ = 'foods'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    brand = db.Column(db.String(100))
    category = db.Column(db.String(30))

    ingredients = db.relationship(
        'Ingredient', secondary=food_ingredient, back_populates='foods')

    notes = db.relationship(
        'Note', back_populates='food', cascade='all, delete')
```

returned JSON result

```JSON
{
    "id": 1,
    "name": "Tuna With Prawn Canned Adult Cat Food",
    "brand": "Applaws",
    "category": "Wet",
    "ingredients": [
        {
            "id": 5,
            "name": "Tuna",
            "category": "Seafood"
        },
        {
            "id": 6,
            "name": "Prawn",
            "category": "Seafood"
        }
    ],
    "notes": []
}
```

marshmallow schema

```python
ingredients = fields.List(fields.Nested(
    'IngredientSchema', exclude=['foods']))
notes = fields.List(fields.Nested('NoteSchema', exclude=[
    'food_id', 'food', 'cat_id']))
```

### Ingredient model

```python
class Ingredient(db.Model):
    __tablename__ = 'ingredients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    category = db.Column(db.String(30))

    foods = db.relationship(
        'Food', secondary=food_ingredient, back_populates='ingredients')
```

returned JSON result

```JSON
{
    "id": 1,
    "name": "Chicken",
    "category": "Meat",
    "foods": [
        {
            "id": 2,
            "name": "Chicken Wet Cat Food Cans",
            "brand": "Ziwi",
            "category": "Wet"
        }
    ]
}
```

marshmallow schema:

```python
foods = fields.List(fields.Nested(
    'FoodSchema', exclude=['notes', 'ingredients']))
```

#### food_ingredient join table

```python
food_ingredient = db.Table('food_ingredient',
                           db.Column('food_id', db.Integer,
                                     db.ForeignKey('foods.id', ondelete='CASCADE'), primary_key=True),
                           db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredients.id', ondelete='CASCADE'), primary_key=True))
```

### Note model

```python
class Note(db.Model):
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String)
    rating = db.Column(db.Integer, default=0)
    date_recorded = db.Column(db.Date, default=date.today())

    cat_id = db.Column(db.Integer, db.ForeignKey(
        'cats.id', ondelete='CASCADE'), nullable=False)
    cat = db.relationship('Cat', back_populates='notes')

    food_id = db.Column(db.Integer, db.ForeignKey(
        'foods.id', ondelete='CASCADE'), nullable=False)
    food = db.relationship('Food', back_populates='notes')
```

returned JSON

```JSON
{
    "id": 1,
    "message": "Luna was ok with it, maybe will try a different one",
    "rating": 0,
    "date_recorded": "2023-06-24",
    "cat": {
        "id": 1,
        "name": "Luna",
        "breed": "Domestic Shorthair",
        "owner": {
            "username": "John"
        }
    },
    "food": {
        "id": 1,
        "name": "Tuna With Prawn Canned Adult Cat Food",
        "brand": "Applaws",
        "category": "Wet",
        "ingredients": [
            {
                "id": 5,
                "name": "Tuna",
                "category": "Seafood"
            },
            {
                "id": 6,
                "name": "Prawn",
                "category": "Seafood"
            }
        ]
    }
}
```

marshmallow schema

```python
    cat = fields.Nested('CatSchema', only=['id', 'name', 'breed', 'owner'])
    food = fields.Nested('FoodSchema', exclude=['notes'])
```

## Project planning and implementation (R10)

### Overall timeline

At the beginning of the project, I've created a [Trello Board](https://trello.com/b/IJJ0hY8f/t2a2-implementation-plan) and set the overall timeline of the project:

- Project planning (by 19 Jun)
- App set up (by 20 Jun)
- MVP features (by 25 Jun)
- Bonus features (by 27 Jun)
- Tests and review (by 29 Jun)
- Documentation (by 30 Jun)
- Submission (by 2 Jul)

### Planning

During planning stage, the following user stories were developed:

- As a user, I want register and log in to record and retrieve my related data.
- As an admin, I want to access a list of all users and create other admins
- As an admin/account owner, I want to view my profile and make edits to make sure my information is up-to-date
- As a cat owner, I want to see a list of all cat foods available
- As a cat owner, I want to create my own food if it is not available in the app
- As an cat owner, I want to make changes to the food to make sure they are accurate, and delete food where neccessary
- As a cat owner, I want to see a list of all cats, and maybe others' cats as well to browse their food preferences
- As a cat owner, I want to add my cat in the system
- As a cat owner, I want to see a list of all notes and any particular note to see how my cat (or anyone else's cat) reacts to any food
- As a cat owner, I want to create notes regarding my cat's reaction to foods
- As a cat owner who created the note, I want to be able to edit or delete it if I see any issues
- As a cat owner, I want to see what ingredients a food contains, to help me find any existing patterns of cat's diet
- As a cat owner, I want to check summary statistics, e.g. how many time I have tried the food to a particular cat and what are their overall reaction to it.

Based on the user stories, I've created a list of routes with core functionalities to get an overall image of the project:

![draft endpoints](/docs/draft-endpoints.png)

I've then added the user stories to the project board:
![Project board as at 19 June](/docs/trello-19Jun.jpg)

I've kept track of bonus features and will come back to them when the core features are implemented:
![draft additional features](/docs/additional-features-plan.png)

I've drafted sample json in vscode to get an idea of expected output, which helps me work on the draft ERD:
![sample json](docs/draft-json.png)
![draft ERD](docs/draft-erd.png)

### Implementing

I've used the API platform Postman to group all routes to one collection to help with testing endpoints and creating documentation:
![routes in postman](docs/routes-in-postman.png)

I've created examples in each request to keep track of error handling:
![postman example](/docs/postman-duplicate-email.png)

I've used Trello board to allocate tasks and deadlines for each user story/feature, in order to keep track of project progress.

![trello tasks](docs/trello-tasks.png)

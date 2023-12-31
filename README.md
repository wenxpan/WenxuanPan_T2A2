# T2A2 - Cat Diet API

## Links

- [Github repo](https://github.com/wenxuan-pan/WenxuanPan_T2A2)
- [Trello Board](https://trello.com/b/IJJ0hY8f/t2a2-implementation-plan)
- [API Documentation](https://documenter.getpostman.com/view/28027782/2s93zB5MTY)

Table of Contents

- [T2A2 - Cat Diet API](#t2a2---cat-diet-api)
  - [Links](#links)
  - [Installation and setup](#installation-and-setup)
  - [R1/R2 - Problem identification and justification](#r1r2---problem-identification-and-justification)
  - [R3 - Database system: benefits and drawbacks](#r3---database-system-benefits-and-drawbacks)
  - [R4 - Functionalities and benefits of an ORM](#r4---functionalities-and-benefits-of-an-orm)
  - [R5 - API endpoints](#r5---api-endpoints)
    - [Auth Routes](#auth-routes)
      - [End-point: /auth/register](#end-point-authregister)
      - [End-point: /auth/login](#end-point-authlogin)
    - [User Routes](#user-routes)
      - [End-point: /users](#end-point-users)
      - [End-point: /users](#end-point-users-1)
      - [End-point: /users/user_id](#end-point-usersuser_id)
      - [End-point: /users/user_id](#end-point-usersuser_id-1)
      - [End-point: /users/user_id](#end-point-usersuser_id-2)
      - [End-point: /users/user_id](#end-point-usersuser_id-3)
    - [Food Routes](#food-routes)
      - [End-point: /foods](#end-point-foods)
      - [End-point: /foods](#end-point-foods-1)
      - [End-point: /foods/food_id](#end-point-foodsfood_id)
      - [End-point: /foods/food_id](#end-point-foodsfood_id-1)
      - [End-point: /foods/food_id](#end-point-foodsfood_id-2)
      - [End-point: /foods/food_id](#end-point-foodsfood_id-3)
    - [Ingredient Routes](#ingredient-routes)
      - [End-point: /ingredients](#end-point-ingredients)
      - [End-point: /ingredients](#end-point-ingredients-1)
      - [End-point: /ingredients/ingredient_id](#end-point-ingredientsingredient_id)
      - [End-point: /ingredients/ingredient_id](#end-point-ingredientsingredient_id-1)
      - [End-point: /ingredients/ingredient_id](#end-point-ingredientsingredient_id-2)
      - [End-point: /ingredients/ingredient_id](#end-point-ingredientsingredient_id-3)
    - [Cat Routes](#cat-routes)
      - [End-point: /cats](#end-point-cats)
      - [End-point: /cats](#end-point-cats-1)
      - [End-point: /cats/cat_id](#end-point-catscat_id)
      - [End-point: /cats/cat_id](#end-point-catscat_id-1)
      - [End-point: /cats/cat_id](#end-point-catscat_id-2)
      - [End-point: /cats/cat_id](#end-point-catscat_id-3)
      - [End-point: cats/cat_id/food](#end-point-catscat_idfood)
    - [Note Routes](#note-routes)
      - [End-point: /notes](#end-point-notes)
      - [End-point: /notes](#end-point-notes-1)
      - [End-point: /notes/note_id](#end-point-notesnote_id)
      - [End-point: /notes/note_id](#end-point-notesnote_id-1)
      - [End-point: /notes/note_id](#end-point-notesnote_id-2)
      - [End-point: /notes/note_id](#end-point-notesnote_id-3)
    - [Error handling](#error-handling)
  - [R6/R9 - ERD and database relations](#r6r9---erd-and-database-relations)
    - [ERD](#erd)
    - [Table - users](#table---users)
    - [Table - cats](#table---cats)
    - [Table - notes](#table---notes)
    - [Table - foods](#table---foods)
    - [Table - ingredients](#table---ingredients)
    - [Join table - food_ingredients](#join-table---food_ingredients)
  - [R7 - Third party services](#r7---third-party-services)
    - [SQLAlchemy (2.0.16) \& Flask-SQLAlchemy (3.0.3)](#sqlalchemy-2016--flask-sqlalchemy-303)
    - [psycopg2 (2.9.6)](#psycopg2-296)
    - [marshmallow (3.19.0) \& Flask-marshmallow (0.15.0)](#marshmallow-3190--flask-marshmallow-0150)
    - [Flask-Bcrypt (1.0.1)](#flask-bcrypt-101)
    - [python-dotenv (1.0.0)](#python-dotenv-100)
    - [Flask-JWT-Extended (4.5.2)](#flask-jwt-extended-452)
  - [R8 - Project models and relationships](#r8---project-models-and-relationships)
    - [User model](#user-model)
    - [Cat model](#cat-model)
    - [Food model](#food-model)
    - [Ingredient model](#ingredient-model)
    - [food_ingredients join table](#food_ingredients-join-table)
    - [Note model](#note-model)
  - [R10 - Project planning and implementation](#r10---project-planning-and-implementation)
    - [Overall timeline](#overall-timeline)
    - [Planning](#planning)
    - [Implementing](#implementing)

## Installation and setup

1. Open terminal and run the PostgreSQL prompt:

   ```
   psql
   ```

2. Create and connect to database:

   ```
   Create DATABASE cat_diet;
   \c cat_diet;
   ```

3. Create a user with password and grant user priviliges:

   ```
   CREATE USER cat_diet_dev WITH PASSWORD 'admin123';
   GRANT ALL PRIVILEGES ON DATABASE cat_diet TO cat_diet_dev;
   ```

4. Open another terminal. Use `cd` command and direct to the `WenxuanPan_T2A2/src` directory

5. Create and activate virtual environment:

   ```
   python3 -m venv .venv
   source .venv/bin/activate
   ```

6. Install dependencies

   ```
   python3 -m pip install -r requirements.txt
   ```

7. Rename `.env.sample` to `.env`, and set the db connection string and JWT secret key:

   ```
   DB_URI=postgresql+psycopg2://cat_diet_dev:admin123@localhost:5432/cat_diet
   JWT_KEY=Your Secret Key
   ```

8. In terminal, create and seed the database, then run the flask app:

   ```
   flask db create
   flask db seed
   flask run
   ```

The server will run on `http://127.0.0.1:5000`.

## R1/R2 - Problem identification and justification

The REST Cat Diet API aims to assist cat owners in tracking and managing their cat's diet and food preferences, as well as monitoring any changes over time, in order to keep a well-balanced diet for their cats.

In particular, the app addresses the following issues:

- **Fussy eating:** Many cats are known to be picky eaters, and it can be challenging for cat owners to identify their cat's favourite and least favourite foods. The app provides a platform for cat owners to record and track their cat's preferences, making it easier for them to choose suitable food options.

- **Health and nutrition**: The [Code of Practice for the Private Keeping of Cats](https://agriculture.vic.gov.au/livestock-and-animals/animal-welfare-victoria/domestic-animals-act/codes-of-practice/code-of-practice-for-the-private-keeping-of-cats#h2-6) sets the following minimum standards regarding nutrition:

  > Cats must be fed a diet that provides proper and sufficient food to maintain good health and meet their physiological needs.
  >
  > Cats are carnivores and must not be fed a purely vegetarian diet.
  >
  > Cats must not be fed a diet consisting purely of fresh meat (including fish).

  To meet these standards, owners can use this app to regularly monitor the food type and ingredients to ensure that their cat receives the necessary nutrients and avoid potential health issues caused by an imbalanced diet.

- **Avoiding overfeeding treats:** Treats are given as rewards for cats, but excessive consumption can lead to weight gain and health issues, and owners might not always realise that they are overfeeding. The app allows cat owners to keep track of treat consumption and review on a regular basis to prevent overfeeding.

- **Identifying allergies or intolerances:** Cats can have allergies or food intolerances, and it may take time for owners to realise and identify specific ingredients or brands that cause adverse reactions in their cats. The app allows users to note down their cat's any resistance or adverse reactions to certain foods or ingredients, which can be helpful during vet consultation and finding solutions. This will also help cat owners remember and avoid purchasing similar products in the future.

## R3 - Database system: benefits and drawbacks

I have chosen PostgreSQL as the database management system, because of the following benefits:

- It is a **free and open source** database management system.
- It is good at **handling large datasets** effectively. It is ACID (Atomicity, Consistency, Isolation, Durability) compliant, which means it ensures the reliability and consistency of the stored data. This helps as the app will be potentially tracking and managing a large number of users, cats, foods, ingredients, and notes. The ability to maintain data integrity and handle complex relationships makes PostgreSQL a suitable choice.
- It is a relational database, which provides a more **structured and organized** approach to store and manage data than a non-relational database. This structure aligns well with the entities in the app. The relational model allows for clear definition of entities and relationships between them, making it easier to establish and maintain data consistency.
- PostgreSQL has an **active community** of developers and users and provides accessible documentation and support. Additionally, PostgreSQL integrates well with various programming languages and frameworks, including Python and Flask for this project using SQLAlchemy as the ORM.

There are some drawbacks to be considered:

- As a relational database system, it may have limitations when it comes to **storing data with varying structures**. Adding new attributes to a record often requires adding a new column to the entire table, which can be less flexible compared to non-relational databases. This drawback might be avoided with careful planning and design, ensuring that the schema reflects all the needed functionalities of the app, instead of users needing to add custom properties later on.
- Data stored in PostgreSQL is **not straightly compatible** with objects in a programming language. This is different to a non-relational database which the data objects are usually in JSON format and can be stored directly in it. In this project, the issue is solved using marshmallow, a serialisation and deserialisation tool that helps convert data to formatted JSON result; it also has the adds-on benefit to validate and sanitize input data.
- In terms of **reading performance**, PostgreSQL might not be as good as other systems such as MySQL. This is because it creates a new system process for each user connected to the database, [allocating a significant amount of memory (approximately 10 MB)](https://aws.amazon.com/compare/the-difference-between-mysql-vs-postgresql) for each connection, whereas MySQL utilizes a single process to handle multiple users, resulting in better performance for applications that primarily involve reading and displaying data to users. However, considering that PostgreSQL still performs better in frequent data updates and concurrent write operations, it remains a suitable option for this project.

Overall, PostgreSQL is well-suited for the content and requirements of the app. It effectively manages the relationships between various entities including users, cats, foods, ingredients, and notes. The relational database structure allows for clear definition of these entities and their relationships, enabling efficient querying and retrieval of related data. For example, the relationships between cats and their owners (users) can be easily established and tracked using foreign key constraints. The ability to store and retrieve complex relationships between entities makes PostgreSQL a suitable choice for this app's content despite its limitations.

## R4 - Functionalities and benefits of an ORM

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

## R5 - API endpoints

For more details and example requests on each endpoint, see [API documentation - Postman version](https://documenter.getpostman.com/view/28027782/2s93zB5MTY#intro)

### Auth Routes

#### End-point: /auth/register

Arguments: None

Description: Creates a user in the database

Authentication: None

Authorization: None

Required fields: email (str), password (str), username (str)

Optional fields: None

**Method: POST**

> ```
> http://127.0.0.1:5000/auth/register
> ```

**Request Body**

```json
{
  "email": "apple@gmail.com",
  "password": "spamegg123",
  "username": "apple"
}
```

**Response: 201**

```json
{
  "id": 4,
  "username": "apple",
  "email": "apple@gmail.com",
  "is_admin": false,
  "joined_since": "2023-06-28",
  "cats": []
}
```

#### End-point: /auth/login

Arguments: None

Description: allows user to login and receive a token for authentication and authorization

Authentication: Email + Password

Authorization: None

Required fields: email (str), password(str)

Optional fields: None

**Method: POST**

> ```
> http://127.0.0.1:5000/auth/login
> ```

**Request Body**

```json
{
  "email": "john@gmail.com",
  "password": "johnisuser123"
}
```

**Response: 200**

```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4NzkzNTM4NCwianRpIjoiY2NlNjIzZDktMzNkYi00MDI5LTk0YzMtYmJjZGY4NzYyNmQ5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjg3OTM1Mzg0LCJleHAiOjE2OTA1MjczODR9.J04Pl0t8DJFDPxVaPLJmXep4j9huLLg0jfe0Mkv552A",
  "user": {
    "id": 1,
    "username": "MaryDev",
    "email": "marydev@gmail.com",
    "is_admin": true,
    "joined_since": "2023-06-20"
  },
  "statistics": {
    "total_cats": 0,
    "total_notes": 0,
    "total_food_reviewed": null
  }
}
```

### User Routes

#### End-point: /users

Arguments: None

Description: Return a list of all users in the database

Authentication: JWT Required

Authorization: Bearer Token (admin)

Required fields: None

Optional fields: None

**Method: GET**

> ```
> http://127.0.0.1:5000/users
> ```

**Response: 200**

```json
[
  {
    "id": 1,
    "username": "MaryDev",
    "email": "marydev@gmail.com",
    "is_admin": true,
    "joined_since": "2023-06-20",
    "cats": []
  },
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
]
```

#### End-point: /users

Arguments: None

Description: Allows admin to create a new user or admin in the database

Authentication: JWT Required

Authorization: Bearer Token (admin)

Required fields: username (str), email (str), password (str)

Optional fields: is_admin (bool)

**Method: POST**

> ```
> http://127.0.0.1:5000/users
> ```

**Request Body**

```json
{
  "username": "newuser",
  "email": "newuser@gmail.com",
  "is_admin": true,
  "password": "default123"
}
```

**Response: 201**

```json
{
  "id": 4,
  "username": "newuser",
  "email": "newuser@gmail.com",
  "is_admin": true,
  "joined_since": "2023-06-30",
  "cats": []
}
```

#### End-point: /users/user_id

Arguments: user id

Description: returns information and statistics of the selected user

Authentication: JWT Required

Authorization: Bearer Token (admin or owner)

Required fields: None

Optional fields: None

**Method: GET**

> ```
> http://127.0.0.1:5000/users/:user_id
> ```

**Response: 200**

```json
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
  ],
  "statistics": {
    "total_cats": 1,
    "total_notes": 5,
    "total_foods_reviewed": 3
  }
}
```

#### End-point: /users/user_id

Arguments: user id

Description: allows owner or admin to update user information of the selected id (except is_admin and joined_since fields)

Authentication: JWT Required

Authorization: Bearer Token (admin or owner)

Required fields: None

Optional fields: username (str), email (str), password (str)

Note: is_admin and joined_since status cannot be changed

**Method: PUT**

> ```
> http://127.0.0.1:5000/users/:user_id
> ```

**Request Body**

```json
{
  "username": "new_name",
  "email": "newmaryemail@gmail.com",
  "password": "newpassword123"
}
```

**Response: 200**

```json
{
  "id": 1,
  "username": "new_name",
  "email": "newmaryemail@gmail.com",
  "is_admin": true,
  "joined_since": "2023-06-20"
}
```

#### End-point: /users/user_id

Arguments: user id (integer)

Description: allows owner or admin to update user information of the selected id (except is_admin and joined_since fields)

Authentication: JWT Required

Authorization: Bearer Token (admin or owner)

Required fields: None

Optional fields: username (str), email (str), password (str)

Note: is_admin and joined_since status cannot be changed

**Method: PATCH**

> ```
> http://127.0.0.1:5000/users/:user_id
> ```

**Request Body**

```json
{
  "username": "new_name",
  "email": "newmaryemail1@gmail.com",
  "password": "newpassword123"
}
```

**Response: 200**

```json
{
  "id": 1,
  "username": "new_name",
  "email": "newmaryemail@gmail.com",
  "is_admin": true,
  "joined_since": "2023-06-20"
}
```

#### End-point: /users/user_id

Arguments: user id (integer)

Description: Allows admin to delete a user from the database

Authentication: JWT Required

Authorization: Bearer Token (admin)

Required fields: None

Optional fields: None

**Method: DELETE**

> ```
> http://127.0.0.1:5000/users/:user_id
> ```

**Response: 200**

```json
{
  "message": "User 2 and related cats and notes deleted"
}
```

### Food Routes

#### End-point: /foods

Arguments: None

Description: returns a list of foods with their ingredients

Authentication: None

Authorization: None

Required fields: None

Optional fields: None

**Method: GET**

> ```
> http://127.0.0.1:5000/foods
> ```

**Response: 200**

```json
[
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
    ]
  },
  {
    "id": 2,
    "name": "Chicken Wet Cat Food Cans",
    "brand": "Ziwi",
    "category": "Wet",
    "ingredients": [
      {
        "id": 1,
        "name": "Chicken",
        "category": "Meat"
      }
    ]
  }
]
```

#### End-point: /foods

Arguments: None

Description: creates a new food in the database

Authentication: JWT Required

Authorization: Bearer Token (logged in user)

Required fields: name (str)

Optional fields: brand (str), category (str), ingredients (list)

**Method: POST**

> ```
> http://127.0.0.1:5000/foods
> ```

**Request Body**

```json
{
  "name": "Cats In The Kitchen Pantry Party Pouch Variety Pack In Gravy Wet Cat Food Pouches",
  "category": "wet",
  "brand": "Weruva",
  "ingredients": [{ "id": 1 }, { "id": 2 }]
}
```

**Response: 201**

```json
{
  "id": 5,
  "name": "Cats In The Kitchen Pantry Party Pouch Variety Pack In Gravy Wet Cat Food Pouches",
  "brand": "Weruva",
  "category": "Wet",
  "ingredients": [
    {
      "id": 1,
      "name": "Chicken",
      "category": "Meat"
    },
    {
      "id": 2,
      "name": "Lamb",
      "category": "Meat"
    }
  ],
  "notes": []
}
```

#### End-point: /foods/food_id

Arguments: food id (integer)

Description: returns food of the selected id

Authentication: None

Authorization: None

Required fields: None

Optional fields: None

**Method: GET**

> ```
> http://127.0.0.1:5000/foods/:food_id
> ```

**Response: 200**

```json
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
  "notes": [
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
      }
    }
  ]
}
```

#### End-point: /foods/food_id

Arguments: food id (integer)

Description: updates food information of the selected id

Authentication: JWT Required

Authorization: Bearer Token (admin)

Required fields: None

Optional fields: name (str), brand (str), category (str), ingredients (list)

**Method: PUT**

> ```
> http://127.0.0.1:5000/foods/:food_id
> ```

**Request Body**

```json
{
  "brand": "new brand",
  "category": "Freeze-dried",
  "name": "new food",
  "ingredients": [{ "id": 1 }]
}
```

**Response: 200**

```json
{
  "id": 1,
  "name": "new food",
  "brand": "new brand",
  "category": "Freeze-dried",
  "ingredients": [
    {
      "id": 1,
      "name": "Chicken",
      "category": "Meat"
    }
  ]
}
```

#### End-point: /foods/food_id

Arguments: food id (integer)

Description: updates food information of the selected id

Authentication: JWT Required

Authorization: Bearer Token (admin)

Required fields: None

Optional fields: name (str), brand (str), category (str), ingredients (list)

**Method: PATCH**

> ```
> http://127.0.0.1:5000/foods/:food_id
> ```

**Request Body**

```json
{
  "brand": "new brand",
  "category": "Freeze-dried",
  "name": "new food",
  "ingredients": [{ "id": 1 }]
}
```

**Response: 200**

```json
{
  "id": 1,
  "name": "new food",
  "brand": "new brand",
  "category": "Freeze-dried",
  "ingredients": [
    {
      "id": 1,
      "name": "Chicken",
      "category": "Meat"
    }
  ]
}
```

#### End-point: /foods/food_id

Arguments: food id (integer)

Description: allows admin to delete a food from database

Authentication: JWT Required

Authorization: Bearer Token (admin)

Required fields: None

Optional fields: None

**Method: DELETE**

> ```
> http://127.0.0.1:5000/foods/:food_id
> ```

**Response: 200**

```json
{
  "message": "Food 1 and related notes deleted"
}
```

### Ingredient Routes

#### End-point: /ingredients

Arguments: None

Description: returns a list of ingredients and related foods

Authentication: None

Authorization: None

Required fields: None

Optional fields: None

**Method: GET**

> ```
> http://127.0.0.1:5000/ingredients
> ```

**Response: 200**

```json
[
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
      },
      {
        "id": 3,
        "name": "Adult Oral Care Dry Cat Food",
        "brand": "Hills Science Diet",
        "category": "Dry"
      }
    ]
  },
  {
    "id": 2,
    "name": "Lamb",
    "category": "Meat",
    "foods": []
  },
  {
    "id": 3,
    "name": "Brown Rice",
    "category": "Grains",
    "foods": [
      {
        "id": 3,
        "name": "Adult Oral Care Dry Cat Food",
        "brand": "Hills Science Diet",
        "category": "Dry"
      }
    ]
  }
]
```

#### End-point: /ingredients

Arguments: None

Description: creates a new ingredient in the database

Authentication: JWT Required

Authorization: Bearer Token (logged in user)

Required fields: name (str)

Optional fields: category (str)

**Method: POST**

> ```
> http://127.0.0.1:5000/ingredients
> ```

**Request Body**

```json
{
  "name": "Beef",
  "category": "Meat"
}
```

**Response: 201**

```json
{
  "id": 8,
  "name": "Beef",
  "category": "Meat"
}
```

#### End-point: /ingredients/ingredient_id

Arguments: ingredient id (integer)

Description: returns ingredient of the selected id

Authentication: None

Authorization: None

Required fields: None

Optional fields: None

**Method: GET**

> ```
> http://127.0.0.1:5000/ingredients/:ingredient_id
> ```

**Response: 200**

```json
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
    },
    {
      "id": 3,
      "name": "Adult Oral Care Dry Cat Food",
      "brand": "Hills Science Diet",
      "category": "Dry"
    }
  ]
}
```

#### End-point: /ingredients/ingredient_id

Arguments: ingredient id (integer)

Description: updates ingredient information of the selected id

Authentication: JWT Required

Authorization: Bearer Token (admin)

Required fields: None

Optional fields: name (str), category (str)

**Method: PUT**

> ```
> http://127.0.0.1:5000/ingredients/:ingredient_id
> ```

**Request Body**

```json
{
  "name": "new name",
  "category": "Other"
}
```

**Response: 200**

```json
{
  "id": 1,
  "name": "new name",
  "category": "Other"
}
```

#### End-point: /ingredients/ingredient_id

Arguments: ingredient id (integer)

Description: updates ingredient information of the selected id

Authentication: JWT Required

Authorization: Bearer Token (admin)

Required fields: None

Optional fields: name (str), category (str)

**Method: PATCH**

> ```
> http://127.0.0.1:5000/ingredients/:ingredient_id
> ```

**Request Body**

```json
{
  "name": "new name",
  "category": "Other"
}
```

**Response: 200**

```json
{
  "id": 1,
  "name": "new name",
  "category": "Other"
}
```

#### End-point: /ingredients/ingredient_id

Arguments: ingredient id (integer)

Description: allows admin to delete an ingredient from database

Authentication: JWT Required

Authorization: Bearer Token (admin)

Required fields: None

Optional fields: None

**Method: DELETE**

> ```
> http://127.0.0.1:5000/ingredients/:ingredient_id
> ```

**Response: 200**

```json
{
  "message": "Ingredient 1 deleted"
}
```

### Cat Routes

#### End-point: /cats

Arguments: None

Description: returns a list of cats and their owner's name

Authentication: None

Authorization: None

Required fields: None

Optional fields: None

**Method: GET**

> ```
> http://127.0.0.1:5000/cats
> ```

**Response: 200**

```json
[
  {
    "id": 1,
    "name": "Luna",
    "breed": "Domestic Shorthair",
    "year_born": 2020,
    "year_adopted": 2021,
    "owner": {
      "username": "John"
    }
  },
  {
    "id": 2,
    "name": "Leo",
    "breed": "Exotic Shorthair",
    "year_born": null,
    "year_adopted": 2022,
    "owner": {
      "username": "Frank"
    }
  },
  {
    "id": 3,
    "name": "Milo",
    "breed": "Ragdoll",
    "year_born": 2015,
    "year_adopted": 2019,
    "owner": {
      "username": "Frank"
    }
  },
  {
    "id": 4,
    "name": "Oreo",
    "breed": "Domestic Longhair",
    "year_born": null,
    "year_adopted": 2019,
    "owner": {
      "username": "Frank"
    }
  }
]
```

#### End-point: /cats

Arguments: None

Description: creates a new cat in the database

Authentication: JWT Required

Authorization: Bearer Token (logged in user)

Required fields: name (str)

Optional fields: breed (str), year_born (int), year_adopted (int)

**Method: POST**

> ```
> http://127.0.0.1:5000/cats
> ```

**Request Body**

```json
{
  "name": "new cat",
  "year_born": "2019",
  "year_adopted": "2020",
  "breed": "British Shorthair"
}
```

**Response: 201**

```json
{
  "id": 5,
  "name": "new cat",
  "breed": "British Shorthair",
  "year_born": 2019,
  "year_adopted": 2020,
  "owner": {
    "username": "Frank"
  }
}
```

#### End-point: /cats/cat_id

Arguments: cat id (integer)

Description: returns cat of the selected id and their owner name and notes

Authentication: None

Authorization: None

Required fields: None

Optional fields: None

**Method: GET**

> ```
> http://127.0.0.1:5000/cats/:cat_id
> ```

**Response: 200**

```json
{
  "id": 1,
  "name": "Luna",
  "breed": "Domestic Shorthair",
  "year_born": 2020,
  "year_adopted": 2021,
  "owner": {
    "username": "John"
  },
  "notes": [
    {
      "id": 1,
      "message": "Luna was ok with it, maybe will try a different one",
      "rating": 0,
      "date_recorded": "2023-06-24",
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
    },
    {
      "id": 2,
      "message": "Luna likes the treats",
      "rating": 1,
      "date_recorded": "2023-06-24",
      "food": {
        "id": 4,
        "name": "Feline Treats Dental Catnip Flavour Tub",
        "brand": "Greenies",
        "category": "Treats",
        "ingredients": [
          {
            "id": 4,
            "name": "Ground Wheat",
            "category": "Grains"
          },
          {
            "id": 7,
            "name": "Chicken Meal",
            "category": "Derivatives"
          }
        ]
      }
    }
  ]
}
```

#### End-point: /cats/cat_id

Arguments: cat id (integer)

Description: update cat information of the selected id

Authentication: JWT Required

Authorization: Bearer Token (admin or owner)

Required fields: None

Optional fields: name (str), breed (str), year_born (int), year_adopted (int)

**Method: PUT**

> ```
> http://127.0.0.1:5000/cats/:cat_id
> ```

**Request Body**

```json
{
  "name": "new name",
  "year_born": "2020",
  "year_adopted": "2021",
  "breed": "new breed"
}
```

**Response: 200**

```json
{
  "id": 4,
  "name": "new name",
  "breed": "new breed",
  "year_born": 2020,
  "year_adopted": 2021,
  "owner": {
    "username": "Frank"
  }
}
```

#### End-point: /cats/cat_id

Arguments: cat id (integer)

Description: update cat information of the selected id

Authentication: JWT Required

Authorization: Bearer Token (admin or owner)

Required fields: None

Optional fields: name (str), breed (str), year_born (int), year_adopted (int)

**Method: PATCH**

> ```
> http://127.0.0.1:5000/cats/:cat_id
> ```

**Request Body**

```json
{
  "name": "new name",
  "year_born": "2020",
  "year_adopted": "2021",
  "breed": "new breed"
}
```

**Response: 200**

```json
{
  "id": 1,
  "name": "new name",
  "breed": "new breed",
  "year_born": 2020,
  "year_adopted": 2021,
  "owner": {
    "username": "John"
  }
}
```

#### End-point: /cats/cat_id

Arguments: cat id (integer)

Description: allows admin or owner to delete a cat from database

Authentication: JWT Required

Authorization: Bearer Token (admin or owner)

Required fields: None

Optional fields: None

**Method: DELETE**

> ```
> http://127.0.0.1:5000/cats/:cat_id
> ```

**Response: 200**

```json
{
  "message": "Cat 2 and related notes deleted"
}
```

#### End-point: cats/cat_id/food

Arguments: cat id (integer)

Description: returns a list of foods eaten by the cat, with statistics on total notes and rating

Authentication: None

Authorization: None

Required fields: None

Optional fields: None

**Method: GET**

> ```
> http://127.0.0.1:5000/cats/:cat_id/food
> ```

**Response: 200**

```json
[
  {
    "food": {
      "id": 2,
      "name": "Chicken Wet Cat Food Cans",
      "brand": "Ziwi",
      "category": "Wet",
      "ingredients": [
        {
          "id": 1,
          "name": "Chicken",
          "category": "Meat"
        }
      ]
    },
    "total_notes": 3,
    "total_rating": 2
  },
  {
    "food": {
      "id": 4,
      "name": "Feline Treats Dental Catnip Flavour Tub",
      "brand": "Greenies",
      "category": "Treats",
      "ingredients": [
        {
          "id": 4,
          "name": "Ground Wheat",
          "category": "Grains"
        },
        {
          "id": 7,
          "name": "Chicken Meal",
          "category": "Derivatives"
        }
      ]
    },
    "total_notes": 1,
    "total_rating": 1
  },
  {
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
    },
    "total_notes": 1,
    "total_rating": 0
  }
]
```

### Note Routes

#### End-point: /notes

Arguments: None

Description: returns a list of notes, each with its related cat and food information

Authentication: None

Authorization: None

Required fields: None

Optional fields: None

**Method: GET**

> ```
> http://127.0.0.1:5000/notes
> ```

**Response: 200**

```json
[
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
  },
  {
    "id": 2,
    "message": "Luna likes the treats",
    "rating": 1,
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
      "id": 4,
      "name": "Feline Treats Dental Catnip Flavour Tub",
      "brand": "Greenies",
      "category": "Treats",
      "ingredients": [
        {
          "id": 4,
          "name": "Ground Wheat",
          "category": "Grains"
        },
        {
          "id": 7,
          "name": "Chicken Meal",
          "category": "Derivatives"
        }
      ]
    }
  }
]
```

#### End-point: /notes

Arguments: None

Description: create a new note in the database

Authentication: JWT Required

Authorization: Bearer Token (logged in user)

Required fields: cat_id (int), food_id (int)

Optional fields: message (str), rating (int), date_recorded (date)

**Method: POST**

> ```
> http://127.0.0.1:5000/notes
> ```

**Request Body**

```json
{
  "cat_id": 1,
  "food_id": 2,
  "message": "cat 1 likes food 2",
  "rating": 0,
  "date_recorded": "2023-06-30"
}
```

**Response: 201**

```json
{
  "id": 10,
  "message": "cat 2 likes food 1",
  "rating": 1,
  "date_recorded": "2023-06-30",
  "cat": {
    "id": 2,
    "name": "Leo",
    "breed": "Exotic Shorthair",
    "owner": {
      "username": "Frank"
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

#### End-point: /notes/note_id

Arguments: note id

Description: returns note of the selected id and the related cat and food information

Authentication: None

Authorization: None

Required fields: None

Optional fields: None

**Method: GET**

> ```
> http://127.0.0.1:5000/notes/:note_id
> ```

**Response: 200**

```json
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

#### End-point: /notes/note_id

Arguments: note id (integer)

Description: updates note information of the selected id

Authentication: JWT Required

Authorization: Bearer Token (admin or owner)

Required fields: None

Optional fields: cat_id (int), food_id (int), message (str), rating (int), date_recorded (date)

**Method: PUT**

> ```
> http://127.0.0.1:5000/notes/:note_id
> ```

**Request Body**

```json
{
  "date_recorded": "2023-05-02",
  "cat_id": 3,
  "food_id": 2,
  "message": "new message",
  "rating": 1
}
```

**Response: 200**

```json
{
  "id": 6,
  "message": "new message",
  "rating": 1,
  "date_recorded": "2023-05-02",
  "cat": {
    "id": 3,
    "name": "Milo",
    "breed": "Ragdoll",
    "owner": {
      "username": "Frank"
    }
  },
  "food": {
    "id": 2,
    "name": "Chicken Wet Cat Food Cans",
    "brand": "Ziwi",
    "category": "Wet",
    "ingredients": [
      {
        "id": 1,
        "name": "Chicken",
        "category": "Meat"
      }
    ]
  }
}
```

#### End-point: /notes/note_id

Arguments: note id (integer)

Description: updates note information of the selected id

Authentication: JWT Required

Authorization: Bearer Token (admin or owner)

Required fields: None

Optional fields: cat_id (int), food_id (int), message (str), rating (int), date_recorded (date)

**Method: PATCH**

> ```
> http://127.0.0.1:5000/notes/:note_id
> ```

**Request Body**

```json
{
  "date_recorded": "2023-05-02",
  "cat_id": 3,
  "food_id": 2,
  "message": "new message",
  "rating": 1
}
```

**Response: 200**

```json
{
  "id": 6,
  "message": "new message",
  "rating": 1,
  "date_recorded": "2023-05-02",
  "cat": {
    "id": 3,
    "name": "Milo",
    "breed": "Ragdoll",
    "owner": {
      "username": "Frank"
    }
  },
  "food": {
    "id": 2,
    "name": "Chicken Wet Cat Food Cans",
    "brand": "Ziwi",
    "category": "Wet",
    "ingredients": [
      {
        "id": 1,
        "name": "Chicken",
        "category": "Meat"
      }
    ]
  }
}
```

#### End-point: /notes/note_id

Arguments: note id (integer)

Description: allows admin or owner to delete a note from database

Authentication: JWT Required

Authorization: Bearer Token (admin or owner)

Required fields: None

Optional fields: None

**Method: DELETE**

> ```
> http://127.0.0.1:5000/notes/:note_id
> ```

**Response: 200**

```json
{
  "message": "Note 1 deleted"
}
```

### Error handling

See more in [Postman documentation](https://documenter.getpostman.com/view/28027782/2s93zB5MTY)

![Endpoints - Error handling](/docs/postman-examples-error-handling.png)

## R6/R9 - ERD and database relations

### ERD

![ERD for Cat Diet API](./docs/erd.png)

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

Attributes:

- food_id: this is a foreign key that references id in the foods table. It is an integer and should not be set null
- ingredient_id: this is a foreign key that references id in the ingredients table. It is an integer and should not be set null. Together with food_id, the two attributes form primary keys of this table.

## R7 - Third party services

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

## R8 - Project models and relationships

There are 5 models in this project: User, Cat, Food, Ingredient, Note, created as python subclasses extending `db.Model`. Inside each model, attributes are set as instances of `db.Column`, and arguments can be passed in to set the primary/foreign key, data types, default value and any restrictions etc.

There is an additional join table food_ingredient (created using `db.Table`) that reflects the many-to-many relationship between Food and Ingredient.

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

- The primary key of the User model is `id`, defined using `primary_key=True`.
- `username`, `email`, `password` and `is_admin` are set as `nullable=False`, meaning they are required fields. If no value of `is_admin` is given, it will be set as default False.
- Instead of `db.ForeignKey`, the User model just has a `db.relationship` with `cats`, representing the one-to-many relationship: one user can have many cats; and as it back populates with the single `owner` in `Cat` model, one cat can only belong to one owner. `cascade='all, delete'` means that the cats will be removed if their owner is deleted.

Example JSON result:

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

- The primary key of the Cat model is `id`, defined using `primary_key=True`.
- `name` is set as `nullable=False`, meaning it is required field; `db.String(100)` means that it must be a string no longer than 100 characters.
- `owner_id` is set as foreign key using `db.ForeignKey` that references to `users.id`, and `ondelete='CASCADE'` means that the cat record will be removed when their owner is deleted
- `owner` represents the one-to-many relationship between cats and users, and it is back referencing the `cats` attribute in User model, in order to establish two-way relationship.
- `notes` is set using `db.relationship`, meaning there is one-to-many relationship between notes and cats, and `cascade='all, delete'` means the note will be deleted when the related cat is deleted

Example JSON result:

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

The nested field of owner and list of notes are created through marshmallow schema:

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
        'Ingredient', secondary=food_ingredients, back_populates='foods')

    notes = db.relationship(
        'Note', back_populates='food', cascade='all, delete')
```

- The primary key of the Food model is `id`, defined using `primary_key=True`.
- `name` is set as `nullable=False, unique=True`, meaning it is required field and there cannot be duplicate names; `db.String(200)` means that it must be a string no longer than 200 characters.
- `ingredients` represents the many-to-many relationship between foods and ingredients (Ingredient model), `secondary=food_ingredients` indicates the join table between the two entities, and it is back referencing the `foods` attribute in Ingredient model
- `notes` is set using `db.relationship`, meaning there is one-to-many relationship between notes and foods, and `cascade='all, delete'` means the note will be deleted when the related food is deleted

Example JSON result:

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

The nested lists of ingredients and notes are created through marshmallow schema:

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
        'Food', secondary=food_ingredients, back_populates='ingredients')
```

- The primary key of the Food model is `id`, defined using `primary_key=True`.
- `name` is set as `nullable=False, unique=True`, meaning it is required field and there cannot be duplicate names; `db.String(100)` means that it must be a string no longer than 100 characters.
- `foods` represents the many-to-many relationship between foods and ingredients (Ingredient model), `secondary=food_ingredients` indicates the join table between the two entities, and it is back referencing the `ingredients` attribute in Food model

Example JSON result:

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

The nested list of foods is created through marshmallow schema:

```python
foods = fields.List(fields.Nested(
    'FoodSchema', exclude=['notes', 'ingredients']))
```

### food_ingredients join table

```python
food_ingredients = db.Table('food_ingredients',
                           db.Column('food_id', db.Integer,
                                     db.ForeignKey('foods.id', ondelete='CASCADE'), primary_key=True),
                           db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredients.id', ondelete='CASCADE'), primary_key=True))
```

- `'food_ingredients'` passed in `db.Table` represents the table name in postgresql database
- column `food_id` is set as the foreign key that references `id` in `foods` table, and `ondelete='CASCADE'` means the food_ingredient record will be deleted if the related food is removed
- column `ingredient_id` is set as the foreign key that references `id` in `ingredients` table, and `ondelete='CASCADE'` means the food_ingredient record will be deleted if the related ingredient is removed
- `food_id` and `ingredient_id` are together set as the primary keys of the table by passing in `primary_key=True` in both columns

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

- The primary key of the Note model is `id`, defined using `primary_key=True`.
- Default values are set for `rating` and `date_recorded` using `default=0` and `default=date.today()`
- `cat_id` and `food_id` are set as foreign keys using `db.ForeignKey` that references to `cats.id` and `foods.id`, and `ondelete='CASCADE'` means that the note record will be removed when the related cat or food is deleted
- `cat` represents the one-to-many relationship between cats and notes, and it is back referencing the `notes` attribute in Cat model, in order to establish two-way relationship.
- `food` represents the one-to-many relationship between foods and notes, and it is back referencing the `notes` attribute in Food model, in order to establish two-way relationship.

Example JSON result:

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

The nested fields of food and cat are created through marshmallow schema:

```python
    cat = fields.Nested('CatSchema', only=['id', 'name', 'breed', 'owner'])
    food = fields.Nested('FoodSchema', exclude=['notes'])
```

## R10 - Project planning and implementation

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

I've drafted sample json in vscode to get an idea of expected output:

![sample json](docs/draft-json.png)

This helps me work on the draft ERD:

![draft ERD](docs/draft-erd.png)

### Implementing

I've used the API platform Postman to group all routes to one collection to help with testing endpoints and creating documentation:

![routes in postman](docs/routes-in-postman.png)

I've created examples in each request to keep track of error handling:

![postman example](/docs/postman-duplicate-email.png)

I've used Trello board to allocate tasks and deadlines for each user story/feature, in order to keep track of project progress.

![trello tasks](docs/trello-tasks.png)

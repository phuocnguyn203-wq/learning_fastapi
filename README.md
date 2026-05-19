# Learning FastAPI With 3-Tier Architecture

This repo is my learning project for FastAPI. I am using it to understand how a backend app can be split into clear layers instead of putting everything in one file.

The main idea I am practicing is **3-tier architecture**:

```text
web layer -> service layer -> data layer
```

I am building small features first, then moving them into the correct layer when I understand what each part should do.

## What I Am Building

This app has two main resources:

- `creature`
- `explorer`

Each resource has its own files in different folders:

```text
app/
  web/       API routes
  service/   business logic layer
  data/      database access layer
  model/     Pydantic models
  fake/      fake in-memory data from earlier learning
```

At the start, I used fake data because it was easier to understand the request and response flow. After that, I started moving the data layer to SQLite so the data can live in a real database file.

## How The 3 Layers Work

### 1. Web Layer

The web layer is where FastAPI routes live.

Example files:

```text
app/web/creature.py
app/web/explorer.py
```

This layer receives HTTP requests like:

```text
GET /creature/all
POST /creature/create
PATCH /explorer/modify
DELETE /explorer/delete
```

What I learned here:

- The route should stay simple.
- It should not know SQL.
- It should call the service layer and return the result.
- `APIRouter` helps split routes into separate files.

The web layer is like the entrance of the app.

## 2. Service Layer

The service layer is between the route and the database.

Example files:

```text
app/service/creature.py
app/service/explorer.py
```

Right now, the service layer is still simple. Most functions just call the data layer:

```python
def create(explorer: Explorer) -> Explorer:
    return explorer_data.create(explorer)
```

What I learned here:

- The service layer keeps the web layer away from database details.
- Later, this is where extra rules can go.
- If the app grows, I do not need to put all logic inside the route function.

This layer helped me understand that even if the code looks small now, the structure matters when the project grows.

## 3. Data Layer

The data layer talks to SQLite.

Example files:

```text
app/data/init.py
app/data/creature.py
app/data/explorer.py
```

This is where I create tables and run SQL queries.

For example, table creation happens in the data file:

```python
curs.execute("""
    create table if not exists explorer(
        name text primary key,
        country text,
        description text)
""")
```

What I learned here:

- SQLite stores data in a file, so data is not new every time I restart the app.
- `create table if not exists` only creates the table if it is missing.
- Top-level Python code runs when the file is imported.
- `fetchone()` reads one row from the cursor. If I call it twice, the second call may return `None`.
- Database errors like duplicate primary keys can be handled with `IntegrityError`.
- Missing data can be turned into an `HTTPException`.

The data layer is where most of my debugging happened because SQL, Python imports, and database state all meet here.

## Models

The models are in:

```text
app/model/creature.py
app/model/explorer.py
```

I use Pydantic models to describe the shape of the data.

Example:

```python
class Explorer(BaseModel):
    name: str
    country: str
    description: str
```

What I learned here:

- Models make request and response data clearer.
- `Explorer` is for full data.
- `ExplorerUpdate` is for partial updates.
- `model_dump()` converts a model into a dictionary that can be passed into SQL parameters.

## My Learning Process

I did not learn this by only reading theory. I learned it by writing code, breaking it, seeing the error, and then understanding why the error happened.

Some examples:

- I learned that importing a file runs its top-level code.
- I learned why the table exists even when I did not manually call a function to create it.
- I learned that the SQLite database file keeps old data.
- I learned that `fetchone()` should be saved into a variable and reused.
- I learned why the data layer should return models instead of raw database rows.
- I learned why route files should not directly contain SQL.

The useful part was not only fixing the error. The useful part was understanding what the error was teaching me about the structure of the app.

## Experience I Extracted

The biggest lesson from this project is that architecture is not only for big applications. Even in a small app, separating the code makes it easier to know where a problem belongs.

When something goes wrong now, I can ask:

- Is this a route problem?
- Is this a service logic problem?
- Is this a database problem?
- Is this a model shape problem?

That makes debugging less random.

I also learned that code can work but still be messy. The goal is not only to make the API respond. The goal is to make the project easier to understand when I come back later.

## Current Flow

For a create request, the flow looks like this:

```text
POST /explorer/create
        |
        v
app/web/explorer.py
        |
        v
app/service/explorer.py
        |
        v
app/data/explorer.py
        |
        v
SQLite database
```

The response then travels back up the same path.

## What I Want To Improve Next

Things I still want to practice:

- Add tests.
- Add a `requirements.txt`.
- Make the data layer cleaner.
- Make update logic more consistent between `creature` and `explorer`.
- Learn when logic should stay in service and when it belongs in data.
- Understand database sessions and connection handling better.

This repo is not only the final code. It is also a record of how I am learning backend structure step by step.

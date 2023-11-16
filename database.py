import sqlalchemy as sql

conn, metadata, humsters = None, None, None

def initDB():
    global conn
    global metadata
    global humsters
    engine = sql.create_engine('sqlite:///humsters.db')
    conn = engine.connect()
    metadata = sql.MetaData()

    humsters = sql.Table('humsters', metadata,
        sql.Column('id', sql.Integer, primary_key = True),
        sql.Column('Photo_link', sql.Text),
        sql.Column('All_ratings', sql.Integer),
        sql.Column('Ratings_count', sql.Integer, default=False)
    )

    metadata.create_all(engine)

def addToDB(link):
    insertion_query = humsters.insert().values({'Photo_link':link, 'All_ratings': 0, 'Ratings_count': 0})
    conn.execute(insertion_query)

def getAllId():
    selection_query = sql.select(humsters).where(humsters.columns.id)
    return [i[0] for i in conn.execute(selection_query).fetchall()]

def selectFromDB(id):
    selection_query = sql.select(humsters).where(humsters.columns.id == id)
    return conn.execute(selection_query).fetchall()

def updateBD(id, rate):
    update_query = sql.update(humsters).where(humsters.columns.id == id).values(All_ratings = selectFromDB(id) + rate)
    conn.execute(update_query)
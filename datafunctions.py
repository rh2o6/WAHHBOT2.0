import psycopg2;
import os

dbpass = os.environ.get('dbpass')
dbname = os.environ.get('dbname')


def opencon():
    connection = psycopg2.connect(host="localhost",dbname=dbname,user = "postgres",password=dbpass,port=5432)
    return connection


def closecon(cn):
    cn.close()


def getallvalues():
    opencon()

    cur = connection.cursor()

    cur.execute("""
                SELECT *
                FROM discordusers
            """)


    connection.commit()
    cur.close()
    connection.close()



def updatecoins(amt,user_id):

    conn = opencon()
    cur = conn.cursor()
    cur.execute("""
                UPDATE discordusers
                SET coins = %s
                WHERE id = %s;
                """,(amt,user_id))
    conn.commit()
    cur.close()
    conn.close()

def updatebank(amt,user_id):
    conn = opencon()
    cur = conn.cursor()
    cur.execute("""
                UPDATE discordusers
                SET bankbalance = %s
                WHERE id = %s;
                """,(amt,user_id))
    conn.commit()
    cur.close()
    conn.close()



def workadjust(amt,user_id):
    conn = opencon()
    cur = conn.cursor()
    cur.execute("""
                UPDATE discordusers
                SET totalshifts = %s
                WHERE id = %s;
                """,(amt,user_id))
    conn.commit()
    cur.close()
    conn.close()


def checkcoins(user_id):
    cc = opencon()
    cr = cc.cursor()
    cr.execute("""SELECT coins FROM discordusers WHERE id = %s""", (user_id,))
    data = cr.fetchone()  # Fetch the result
    cr.close()
    closecon(cc)
    balance = data[0]
    return balance

def checkbankbal(user_id):
    cc = opencon()
    cr = cc.cursor()
    cr.execute("""SELECT bankbalance FROM discordusers WHERE id = %s""",(user_id,))
    data = cr.fetchone()
    cr.close()
    closecon(cc)
    balance = data[0]
    return balance


def checkbanklvl(user_id):
    cc = opencon()
    cr = cc.cursor()
    cr.execute("""SELECT banklvl FROM discordusers WHERE id = %s""",(user_id,))
    data = cr.fetchone()
    cr.close()
    closecon(cc)
    balance = data[0]
    return balance




def checktotalshifts(user_id):
    cc = opencon()
    cr = cc.cursor()
    cr.execute("""SELECT totalshifts FROM discordusers WHERE id = %s""", (user_id,))
    data = cr.fetchone()  # Fetch the result
    cr.close()
    closecon(cc)
    totalshifts = data[0]
    return totalshifts

def userdbcheck(user_id):
    if not userexists(user_id):
        adduser(user_id)



def adduser(user_id):
    conn = opencon()
    cur = conn.cursor()
    # Assuming a very simple table structure; adjust as necessary.
    cur.execute("INSERT INTO discordusers (id, coins, banklvl, bankbalance) VALUES (%s, %s,%s,%s);", (user_id, 0,1,0))
    conn.commit()
    cur.close()
    conn.close()



def userexists(user_id):
    conn = opencon()
    cur = conn.cursor()
    cur.execute("SELECT EXISTS(SELECT 1 FROM discordusers WHERE id = %s);", (user_id,))
    exists = cur.fetchone()[0]
    cur.close()
    conn.close()
    return exists

def register_user_in_fishbucket(user_id: int):
    conn = opencon()
    cur = conn.cursor()

    # Check if the user already exists in the fishbucket table
    cur.execute("""
        SELECT EXISTS(
            SELECT 1
            FROM fishbucket
            WHERE discord_id = %s
        );
    """, (user_id,))
    exists = cur.fetchone()[0]

    if not exists:
        # Insert a new row for the user with default values (0 for all fish)
        cur.execute("""
            INSERT INTO fishbucket (discord_id)
            VALUES (%s);
        """, (user_id,))

    conn.commit()
    cur.close()
    conn.close()

def updatefishbucket(user_id: int, fishtostore: str, fishamt: int):
    # Ensure the user is registered in the fishbucket table
    register_user_in_fishbucket(user_id)

    conn = opencon()
    cur = conn.cursor()

    # Dynamically construct the query with the column name
    query = f"UPDATE fishbucket SET \"{fishtostore}\" = %s WHERE discord_id = %s;"
    cur.execute(query, (fishamt, user_id))

    conn.commit()
    cur.close()
    conn.close()

def checkfishamt(user_id:int, fishtocheck:str):
    conn = opencon()
    cur = conn.cursor()
    cur.execute("SELECT %s from fishbucket WHERE id = %s",(fishtocheck,user_id))

def checkrod(user_id:int):
    conn = opencon()
    cur = conn.cursor()
    cur.execute("SELECT rodtype FROM inventory where id = %s",(user_id,))
    data = cur.fetchone()
    cur.close()
    closecon(conn)
    balance = data[0]
    return balance




def getfishbucket(user_id: int):
    conn = opencon()
    cur = conn.cursor()
    register_user_in_fishbucket(user_id)  # Ensure the user exists in the table

    # Query to fetch all columns for the given user_id
    cur.execute("""
        SELECT *
        FROM fishbucket
        WHERE discord_id = %s;
    """, (user_id,))

    row = cur.fetchone()  # Fetch the single row for the user
    cur.close()
    conn.close()

    if not row:
        # If no row exists for the user, return an empty dictionary
        return {}

    # Get column names dynamically
    column_names = [desc[0] for desc in cur.description]

    # Create a dictionary excluding the 'discord_id' column
    fish_bucket = {column_names[i]: row[i] for i in range(len(column_names)) if column_names[i] != 'discord_id'}
    return fish_bucket



def create_or_update_fishbucket_table():
    conn = opencon()
    cur = conn.cursor()

    # Get all fish names from content.fish_data["categories"]
    import content  # Importing here to avoid circular imports
    fish_categories = content.fish_data["categories"]
    all_fish = set()
    for tier, fish_list in fish_categories.items():
        all_fish.update(fish_list)

    # Ensure the table exists
    create_table_query = """
    CREATE TABLE IF NOT EXISTS fishbucket (
        discord_id BIGINT PRIMARY KEY
    );
    """
    cur.execute(create_table_query)

    # Get existing columns in the table
    cur.execute("""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = 'fishbucket';
    """)
    existing_columns = {row[0].lower() for row in cur.fetchall()}  # Convert to lowercase for case-insensitive comparison

    # Add missing columns
    for fish in all_fish:
        if fish.lower() not in existing_columns:  # Compare in lowercase
            alter_table_query = f"""
            ALTER TABLE fishbucket
            ADD COLUMN "{fish}" INT DEFAULT 0;
            """
            cur.execute(alter_table_query)

    conn.commit()
    cur.close()
    conn.close()
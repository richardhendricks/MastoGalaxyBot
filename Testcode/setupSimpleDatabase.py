import sqlite3
from sqlite3 import Error

Debug = True

def printError(e):
    if Debug: print(f"The error '{e}' occurred")

def create_connection(path):
    connection=None
    try:
        connection = sqlite3.connect(path)
        if Debug: print("Connection to SQLite DB successful")
    except Error as e:
        printError(e)
    
    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        if Debug: print("Query executed succesfully")
    except Error as e:
        printError(e)

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        printError(e)

create_images_table = """
CREATE TABLE IF NOT EXISTS images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    url TEXT NOT NULL,
    url_raw TEXT NOT NULL,
    tags TEXT NOT NULL,
    shooting_params TEXT NOT NULL,
    alt_text TEXT NOT NULL,
    info TEXT NOT NULL,
    recent INTEGER NOT NULL
);
"""

create_tags_table = """
CREATE TABLE IF NOT EXISTS tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);
"""

create_image_tags_table = """
CREATE TABLE IF NOT EXISTS image_tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    image_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    FOREIGN KEY (tag_id) REFERENCES tags (id),
    FOREIGN KEY (image_id) REFERENCES images (id)
);
"""

create_images="""
INSERT INTO
    images (name, url, url_raw, tags, shooting_params, alt_text, info, recent)
VALUES
    ('M31', 'http:blah-m31', 'http://blahblah.com/m31-raw', 'spiral local_group large', '180sx15 AT125EDL Canon SL1 HAE43EC', 'something descriptive', 'something from wikipedia', 0),
    ('IC10', 'http:blah-IC10', 'http://blahblah.com/IC10-raw', 'local_group starburst irregular small', '180sx15 AT125EDL Canon SL1 HAE43EC', 'something descriptive', 'something from wikipedia', 0),
    ('M33', 'http:blah-m33', 'http://blahblah.com/m33-raw', 'spiral local_group', '180sx15 AT125EDL Canon SL1 HAE43EC', 'something descriptive', 'something from wikipedia', 0);
"""

# Normally the entries in this table will be generated from tags collected in the images database
create_tags="""
INSERT INTO
    tags (name)
VALUES
    ('spiral'),
    ('local_group'),
    ('large'),
    ('starburst'),
    ('irregular'),
    ('small');
"""

# Normally the entries in this table will be generated from images database
create_image_tags = """
INSERT INTO
    image_tags (image_id, tag_id)
VALUES
    ('1', '1'),
    ('1', '2'),
    ('1', '3'),
    ('2', '2'),
    ('2', '4'),
    ('2', '5'),
    ('2', '6'),
    ('3', '1'),
    ('3', '2');
"""

# Choose a random image that has not been recently used
select_image_random = """
SELECT * FROM images 
WHERE
    recent = 0
ORDER BY RANDOM() 
LIMIT 1;
"""

# Print all images and their age
select_image_age = """
SELECT 
    id, name, recent
FROM
    images;
"""

# Update image "recent" tag to 3, will not select image for 3 iterations
mark_image_recent = """
UPDATE images
SET recent = 3
WHERE id = """

# reduce all recent non-zero entries by 1
reduce_image_recent ="""
UPDATE images
SET recent = recent - 1
WHERE recent > 0;
"""


# Main portion of program

connection = create_connection(":memory:")

execute_query(connection, create_images_table)
execute_query(connection, create_tags_table)
execute_query(connection, create_image_tags_table)
execute_query(connection, create_images)
execute_query(connection, create_tags)
execute_query(connection, create_image_tags)

print("Printing all images + recent age")
image = execute_read_query(connection, select_image_age)
print(image)

print("Printing a random image")
image = execute_read_query(connection, select_image_random)
print(image)

print("Marking image " + str(image[0][0]) + " as recently used")
mark_image_recent_full_query = mark_image_recent + str(image[0][0]) + ";"  # sanitize this?
execute_query(connection, mark_image_recent_full_query)

image = execute_read_query(connection, select_image_random)
print(image)
image = execute_read_query(connection, select_image_random)
print(image)
image = execute_read_query(connection, select_image_random)
print(image)
image = execute_read_query(connection, select_image_random)
print(image)
image = execute_read_query(connection, select_image_random)
print(image)

print("Aging all recently used images")
image = execute_query(connection, reduce_image_recent)
print("Printing all images + recent age")
image = execute_read_query(connection, select_image_age)
print(image)

print("Aging all recently used images a second time")
image = execute_query(connection, reduce_image_recent)
print("Printing all images + recent age")
image = execute_read_query(connection, select_image_age)
print(image)

print("Aging all recently used images a third time")
image = execute_query(connection, reduce_image_recent)
print("Printing all images + recent age")
image = execute_read_query(connection, select_image_age)
print(image)
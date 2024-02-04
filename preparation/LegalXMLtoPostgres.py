import xml.etree.ElementTree as ET
import psycopg2
import logging

# Logging configuration
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# Database connection information
dbname = "your_dbname"
user = "your_username"
password = "your_password"
host = "your_host"

# Path to your XML file
xml_file_path = 'your_data.xml'

def parse_xml_and_insert_to_db(xml_file_path, dbname, user, password, host):
    try:
        # Load and parse the XML file
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        # Connect to the database
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
        cur = conn.cursor()

        # Parse XML data and insert into the database
        for part in root.findall('Part'):
            part_title = part.find('PartTitle').text
            # Insert part title into Parts table and get the part_id
            cur.execute("INSERT INTO Parts (title) VALUES (%s) RETURNING part_id", (part_title,))
            part_id = cur.fetchone()[0]

            for chapter in part.findall('Chapter'):
                chapter_num = chapter.get('Num')
                chapter_title = chapter.find('ChapterTitle').text
                # Insert chapter data into Chapters table and get the chapter_id
                cur.execute("INSERT INTO Chapters (part_id, num, title) VALUES (%s, %s, %s) RETURNING chapter_id", (part_id, chapter_num, chapter_title))
                chapter_id = cur.fetchone()[0]

                # Similarly, parse and insert Articles, Paragraphs, Sentences, Items into the database
                # ...

        # Commit the changes
        conn.commit()

    except Exception as e:
        # Log any errors that occur
        logging.error("Error occurred", exc_info=True)
    finally:
        # Close the connection
        if conn:
            cur.close()
            conn.close()

# Execute the script
parse_xml_and_insert_to_db(xml_file_path, dbname, user, password, host)

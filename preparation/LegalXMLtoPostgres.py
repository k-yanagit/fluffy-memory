"""
XML to PostgreSQL Importer

This program provides a class, XMLToPostgreSQL, designed to facilitate the import of data from an XML file into a PostgreSQL database table. It creates the necessary table based on provided schema and inserts data from the XML file into the table.

Usage:
1. Instantiate the XMLToPostgreSQL class with appropriate parameters.
2. Call the import_data() method to perform the data import.

Example:
    # Define PostgreSQL database connection parameters
    db_params = {
        'host': 'localhost',
        'database': 'mydb',
        'user': 'myuser',
        'password': 'mypassword'
    }

    # Define the XML file path, table name, and table columns
    xml_file_path = 'data.xml'
    table_name = 'mytable'
    table_columns = {
        'column1': 'TEXT',
        'column2': 'INTEGER',
        'column3': 'TEXT'
        # Add more columns as needed
    }

    # Instantiate the XMLToPostgreSQL class
    xml_importer = XMLToPostgreSQL(db_params, xml_file_path, table_name, table_columns)

    # Import data into PostgreSQL
    xml_importer.import_data()
"""

import psycopg2
import xml.etree.ElementTree as ET

class XMLToPostgreSQL:
    def __init__(self, db_params, xml_file_path, table_name, table_columns):
        """
        Initialize the XMLToPostgreSQL class with the necessary parameters.

        Args:
            db_params (dict): Dictionary containing database connection parameters.
            xml_file_path (str): Path to the XML file to be imported.
            table_name (str): Name of the PostgreSQL table where data will be inserted.
            table_columns (dict): Dictionary mapping column names to their data types.
        """
        self.db_params = db_params
        self.xml_file_path = xml_file_path
        self.table_name = table_name
        self.table_columns = table_columns

    import psycopg2
import xml.etree.ElementTree as ET

class LegalXMLtoPostgres:
    def __init__(self, db_params, xml_file_path):
        self.db_params = db_params
        self.xml_file_path = xml_file_path

    def create_table(self, cur):
        # Generate SQL query to create the table if it doesn't exist
        create_table_query = """
        CREATE TABLE IF NOT EXISTS LegalData (
            LawID SERIAL PRIMARY KEY,
            Era VARCHAR,
            Lang VARCHAR,
            LawType VARCHAR,
            Num VARCHAR,
            Year INT,
            PromulgateMonth INT,
            PromulgateDay INT,
            Kana VARCHAR,
            Abbrev VARCHAR,
            AbbrevKana VARCHAR,
            Title VARCHAR,
            TOCLabel VARCHAR,
            TOCNum INT,
            PartTitle VARCHAR,
            ChapterNum INT,
            ChapterTitle VARCHAR,
            ArticleNum VARCHAR,
            ArticleCaption VARCHAR,
            ArticleTitle VARCHAR,
            ParagraphNum INT,
            ParagraphSentence TEXT
        );
        """

        cur.execute(create_table_query)

    def import_data(self):
        try:
            # Connect to PostgreSQL
            conn = psycopg2.connect(**self.db_params)
            cur = conn.cursor()

            # Create the table
            self.create_table(cur)

            # Parse the XML file
            tree = ET.parse(self.xml_file_path)
            root = tree.getroot()

            for law in root.findall(".//Law"):
                data = {
                    'Era': law.find('Era').text,
                    'Lang': law.find('Lang').text,
                    'LawType': law.find('LawType').text,
                    'Num': law.find('Num').text,
                    'Year': int(law.find('Year').text),
                    'PromulgateMonth': int(law.find('PromulgateMonth').text),
                    'PromulgateDay': int(law.find('PromulgateDay').text),
                    'Kana': law.find('Kana').text,
                    'Abbrev': law.find('Abbrev').text,
                    'AbbrevKana': law.find('AbbrevKana').text,
                    'Title': law.find('Title').text,
                    'TOCLabel': law.find('.//TOCLabel').text,
                    'TOCNum': int(law.find('.//TOCNum').text),
                    'PartTitle': law.find('.//PartTitle').text,
                    'ChapterNum': int(law.find('.//ChapterNum').text),
                    'ChapterTitle': law.find('.//ChapterTitle').text,
                    'ArticleNum': law.find('.//ArticleNum').text,
                    'ArticleCaption': law.find('.//ArticleCaption').text,
                    'ArticleTitle': law.find('.//ArticleTitle').text,
                    'ParagraphNum': int(law.find('.//ParagraphNum').text),
                    'ParagraphSentence': law.find('.//ParagraphSentence').text
                }

                # Generate SQL query to insert data into the table
                insert_query = """
                INSERT INTO LegalData (
                    Era, Lang, LawType, Num, Year, PromulgateMonth, PromulgateDay,
                    Kana, Abbrev, AbbrevKana, Title, TOCLabel, TOCNum, PartTitle,
                    ChapterNum, ChapterTitle, ArticleNum, ArticleCaption, ArticleTitle,
                    ParagraphNum, ParagraphSentence
                ) VALUES (
                    %(Era)s, %(Lang)s, %(LawType)s, %(Num)s, %(Year)s, %(PromulgateMonth)s, %(PromulgateDay)s,
                    %(Kana)s, %(Abbrev)s, %(AbbrevKana)s, %(Title)s, %(TOCLabel)s, %(TOCNum)s, %(PartTitle)s,
                    %(ChapterNum)s, %(ChapterTitle)s, %(ArticleNum)s, %(ArticleCaption)s, %(ArticleTitle)s,
                    %(ParagraphNum)s, %(ParagraphSentence)s
                );
                """
                cur.execute(insert_query, data)

            # Commit the transaction
            conn.commit()

        except Exception as e:
            print(f"Error: {e}")
        finally:
            # Close the connection and perform cleanup
            cur.close()
            conn.close()

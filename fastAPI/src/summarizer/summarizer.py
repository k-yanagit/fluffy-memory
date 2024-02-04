"""
LegalTextProcessor Program File
This program uses the BART model to process legal texts. It connects to a PostgreSQL database to retrieve predefined legal term explanations.
If an explanation is not found in the database, it uses the BART model to generate a description for the given legal term or text.
"""

from transformers import BartForConditionalGeneration, BartTokenizer
from databases import Database

# Database connection configuration
DATABASE_URL = "postgresql://user:password@localhost/dbname"

class LegalTextProcessor:
    """
    A processor for legal texts using the BART model.
    It can retrieve explanations for legal terms from a PostgreSQL database
    or generate descriptions for legal terms or texts using the BART model.
    """
    def __init__(self):
        """
        Initializes the BART model, tokenizer, and database connection.
        """
        self.model_name = 'facebook/bart-large-cnn'
        self.tokenizer = BartTokenizer.from_pretrained(self.model_name)
        self.model = BartForConditionalGeneration.from_pretrained(self.model_name)
        self.database = Database(DATABASE_URL)

    async def _connect_to_db(self):
        """
        Connects to the PostgreSQL database.
        """
        await self.database.connect()

    async def _disconnect_from_db(self):
        """
        Disconnects from the PostgreSQL database.
        """
        await self.database.disconnect()

    async def generate_description(self, text: str) -> str:
        """
        Generates a description for a legal term or text using the BART model.
        :param text: The legal term or text for which to generate a description.
        :return: The generated description.
        """
        inputs = self.tokenizer([text], max_length=1024, return_tensors='pt')
        summary_ids = self.model.generate(inputs['input_ids'], num_beams=4, max_length=200, early_stopping=True)
        description = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return description

    async def process_text(self, text: str) -> str:
        """
        Processes the input text by first checking for a predefined explanation in the database.
        If not found, it generates a description using the BART model.
        :param text: The legal term or text to process.
        :return: The explanation or generated description of the text.
        """
        # Ensure the database connection is established
        await self._connect_to_db()
        try:
            db_result = await self._get_legal_explanation(text)
            if db_result:
                return db_result
            else:
                description = await self.generate_description(text)
                return description
        finally:
            # Ensure the database connection is properly closed
            await self._disconnect_from_db()

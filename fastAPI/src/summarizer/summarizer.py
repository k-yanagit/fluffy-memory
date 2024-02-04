"""
LegalTextProcessor Program File
This program uses the BART model to process legal texts. It connects to a PostgreSQL database to retrieve predefined legal term explanations.
If an explanation is not found in the database, it uses the BART model to generate a description for the given legal term or text.
"""

from transformers import BartForConditionalGeneration, BartTokenizer, T5ForConditionalGeneration, T5Tokenizer, GPT2LMHeadModel, GPT2Tokenizer
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
        self.gpt2_model_name = 'rinna/japanese-gpt2-medium'
        self.gpt2_tokenizer = GPT2Tokenizer.from_pretrained(self.gpt2_model_name)
        self.gpt2_model = GPT2LMHeadModel.from_pretrained(self.gpt2_model_name)

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

    async def _simplify_description(self, description: str) -> str:
        """
        Simplifies the language of the description using the Japanese GPT-2 model.
        :param description: The legal description or generated text.
        :return: A simplified version of the description.
        """
        # Prepare the text for the GPT-2 model
        input_ids = self.gpt2_tokenizer.encode(description, return_tensors='pt', max_length=512, truncation=True)

        # Generate the simplified description
        outputs = self.gpt2_model.generate(input_ids, max_length=200, num_beams=4, early_stopping=True)
        simplified_description = self.gpt2_tokenizer.decode(outputs[0], skip_special_tokens=True)

        return simplified_description

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
                simple_description = self._simplify_description(db_result)
                return simple_description
            else:
                description = await self.generate_description(text)
                simple_description = self._simplify_description(description)
                return simple_description
        finally:
            # Ensure the database connection is properly closed
            await self._disconnect_from_db()

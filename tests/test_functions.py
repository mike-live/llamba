from llamba.chatmodels.chat_model import AbstractChatModel
import unittest

class TestAnalyzeFunction(unittest.TestCase):
    def test_query(self):
        # Prepare a Chatbot model
        class DummyChatModel(AbstractChatModel): pass
        chat_model = DummyChatModel()
        res = chat_model.query("What is 2 + 2?")
        self.assertEqual(res[0], False)

if __name__ == '__main__':
    unittest.main()
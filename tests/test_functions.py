from llamba import chat_model
from llamba import connector

# Test for local machine only, since API keys can't be transferred to github safely
# Possible workaround -- self-hosted test runner
def test_query():
    chatbot = connector.ChatModel(url="<URL>", api_key="AAAA", chatbot_id="BBBB")
    res = chatbot.query('What does an increased level of albumin mean?')
    assert res[0] == False
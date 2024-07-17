from llamba.chat_model import ChatbaseModel

# Test for local machine only, since API keys can't be transferred to github safely
# Possible workaround -- self-hosted test runner
def test_query():
    chatbot = ChatbaseModel(url="<URL>", api_key="AAAA", chatbot_id="BBBB")
    res = chatbot.query('What does an increased level of albumin mean?')
    assert res[0] == False
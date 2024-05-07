from bioage_framework import functions
from bioage_framework import classes

# Test for local machine only, since API keys can't be transferred to github safely
# Possible workaround -- self-hosted test runner
def test_query():
    chatbot = classes.ChatModel(url="<URL>", api_key="AAAA", chatbot_id="BBBB")
    res = chatbot.query('What does an increased level of albumin mean?')
    assert res[0] == False
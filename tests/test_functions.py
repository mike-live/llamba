from bioage_framework import functions
from bioage_framework import classes
import config

def test_query():
    chatbot = classes.ChatModel(url=config.URL_CB, api_key=config.API_KEY_CB, chatbot_id=config.ID_CB)
    print(chatbot.headers)
    res = chatbot.query('What does an increased level of albumin mean?')
    print(res)
    assert res[0] == True
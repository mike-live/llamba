from bioage_framework import functions
from bioage_framework import classes

def test_initialize():
    assert functions.initialize(object(), classes.ChatModel(url="http://localhost:3030", api_key="123xyz")
    ) == classes.Connector((object(), classes.ChatModel(url="http://localhost:3030", api_key="123xyz")))

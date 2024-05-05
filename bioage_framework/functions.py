from math import radians, cos, sin, asin, sqrt
from classes import ChatModel, Connector

def initialize(bioage_model: object, llm_chat: ChatModel):
    return Connector(bioage_model, llm_chat)
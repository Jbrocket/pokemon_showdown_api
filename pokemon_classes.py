import re
import collections
from db_manager import Base
from sqlalchemy import Column, Integer, String, Boolean, Float

class Pokemon(Base):
    __tablename__ = 'pokemon'
    poke_id = Column(Integer, primary_key=True)
    name = Column(String)
    type1 = Column(String)
    type2 = Column(String)
    link_normal = Column(String)
    link_shiny = Column(String)
    atk = Column(Integer)
    df = Column(Integer)
    spatk = Column(Integer)
    spdf = Column(Integer)
    speed = Column(Integer)
    hp = Column(Integer)
    
    def __init__(self, name: str, type1: str, type2: str, link_normal: str, link_shiny: str, atk: int, df: int, spatk: int, spdf: int, speed:int, hp: int):
        self.name = name
        self.type1 = type1
        self.type2 = type2
        self.link_normal = link_normal
        self.link_shiny = link_shiny
        self.atk = atk
        self.df = df
        self.spatk = spatk
        self.spdf = spdf
        self.speed = speed
        self.hp = hp
        self.counter = 0
        self.moves = {}
        
class Move(Base):
    __tablename__ = "moves"
    move_id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    accuracy = Column(Float)
    damage = Column(Integer)
    pp = Column(Integer)
    priority = Column(Integer)
    
    def __init__(self, name: str, type: str, accuracy: float, damage: int, pp: int, priority: int):
        self.name = name
        self.type = type
        self.accuracy = accuracy
        self.damage = damage
        self.pp = pp
        self.priority = priority
        
        
class Stats:
    def __init__(self, id):
        self.id = id
        self.games = collections.defaultdict(lambda: None)
        self.pokemon_list = collections.defaultdict(lambda: None)
    
class PlayerStats(Stats):
    def __init__(self, id):
        Stats.__init__(self, id)

class FormatStats(Stats):
    def __init__(self, id):
        Stats.__init__(self, id)
import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base


engine = create_engine('sqlite:///pokemon.sqlite')
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():

    from pokemon_classes import Pokemon, Move
    Base.metadata.create_all(bind=engine, checkfirst=True)
    pokemon_list = []
    move_list = []
        
    with open('pokemon_info.csv', newline='') as csvfile:
        pokemon_csv = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in pokemon_csv:
            # print(row)
            pokemon_list.append(Pokemon(name=row[0], type1=row[1], type2=row[2], link_normal=row[3], link_shiny=row[4], atk=int(row[5]), df=int(row[6]), spatk=int(row[7]), spdf=int(row[8]), speed=int(row[9]), hp=int(row[10])))
    
    with open('move_info.csv', newline='') as csvfile:
        move_csv = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in move_csv:
            # print(row)
            move_list.append(Move(name=row[0], type=row[1], accuracy=float(row[2]) if row[2] else 0, damage=int(row[3]) if row[3] else 0, pp=int(row[4]) if row[4] else 0, priority=int(row[5] if row[5] else 0)))
    # save the database
    for pokemon in pokemon_list:
        db_session.add(pokemon)
    for move in move_list:
        db_session.add(move)
    db_session.commit()

if __name__== "__main__":
    init_db()
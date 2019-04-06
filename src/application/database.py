from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import scoped_session, sessionmaker
import mysql.connector

#反射数据库所有的表
Base = automap_base()

# 初始化数据库连接:
engine = create_engine('mysql+mysqlconnector://root:314159@localhost/SpeechCollection', pool_recycle=3600)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base.prepare(engine, reflect=True)

Speech_sheet = Base.classes.speech_sheet
Speaker_sheet = Base.classes.speaker_sheet
Word_sheet = Base.classes.word_sheet
Speaker_sheet = Base.classes.speaker_sheet
Sentence_sheet = Base.classes.sentence_sheet
Word_position_sheet = Base.classes.word_position_sheet
Part_of_speech_sheet = Base.classes.part_of_speech_sheet
Depend_synta_re_sheet = Base.classes.depend_synta_re_sheet
Named_entity_sheet = Base.classes.named_entity_sheet
Semant_role_type_sheet = Base.classes.semant_role_type_sheet



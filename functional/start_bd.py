from sqlalchemy import (MetaData, Table, Column, Integer, String, Text, ForeignKey, create_engine,
                         insert, text, Float, DateTime)
from sqlalchemy.orm import declarative_base, Session
from datetime import datetime


Base = declarative_base()

engine = create_engine(
    "sqlite:///bd/mybd.sqlite3",
    echo=True
)

metadata = MetaData()


class User(Base):
    __tablename__ = "users"
    tg_id = Column(Integer(), primary_key=True)
    name = Column(String(200), nullable=False)
    status = Column(String)
    date = Column(DateTime, default=datetime.now)



class Subject(Base):
    __tablename__ = "subjects"
    id = Column(Integer(), primary_key=True)
    subject = Column(String)



class Topic(Base):
    __tablename__ = "topics"
    id = Column(Integer(), primary_key=True)
    subject_id = Column(ForeignKey("subjects.id", ondelete="CASCADE"))
    title = Column(String)
    theory = Column(String)

class Test(Base):
    __tablename__ = 'tests'
    id = Column(Integer(), primary_key=True)
    topics_id = Column(ForeignKey("topics.id", ondelete="CASCADE"))
    question = Column(String)
    answer = Column(String)

class User_result(Base):
    __tablename__ = 'user_results'
    id = Column(Integer(), primary_key=True)
    tg_id = Column(ForeignKey("users.tg_id", ondelete="CASCADE"))
    topic_id = Column(ForeignKey("topics.id", ondelete="CASCADE"))
    result = Column(String)

Base.metadata.create_all(engine)



def delete_users():
    with engine.begin()as conn:
        conn.execute(text("DELETE FROM users"))

def delete_subjects():
    with engine.begin()as conn:
        conn.execute(text("DELETE FROM subjects"))

def delete_topics():
    with engine.begin()as conn:
        conn.execute(text("DELETE FROM topics"))

def delete_tests():
    with engine.begin()as conn:
        conn.execute(text("DELETE FROM tests"))

def delete_user_results():
    with engine.begin()as conn:
        conn.execute(text("DELETE FROM user_results"))


def new_user(id_user: int =0, name: str ='', status: str =''):
    with Session(engine) as session:
        new_user = User(tg_id=id_user, name=name, status=status)
        session.add(new_user)
        session.commit()

def new_subject(subject: str =''):
    with Session(engine) as session:
        new_subject = Subject(subject=subject)
        session.add(new_subject)
        session.commit()

def new_topic(subject_id: int =1, title: str ='', theory: str =''):
    with Session(engine) as session:
        new_topic = Topic(subject_id=subject_id, title=title, theory=theory)
        session.add(new_topic)
        session.commit()

def new_test(topics_id: int =1, question: str ='', answer: str =''):
    with Session(engine) as session:
        new_test = Test(topics_id=topics_id, question=question, answer=answer)
        session.add(new_test)
        session.commit()

def new_user_result(tg_id: int =1, topic_id: int =1, result: str =''):
    with Session(engine) as session:
        new_user_result = User_result(tg_id=tg_id, topic_id=topic_id, result=result)
        session.add(new_user_result)
        session.commit()

# delete_users()
# delete_subjects()
# delete_topics()
# delete_tests()
# delete_user_results()

# new_user()
# new_subject()

# new_topic(subject_id=3, title='отечественная война 1812 года', theory='''Отечественная война 1812 года — военный конфликт между Российской империей и наполеоновской Францией, длившийся с июня по декабрь 1812 года. Война завершилась полным разгромом французской армии и изгнанием захватчиков с территории России. 
# Причины войны
# Отказ России от соблюдения континентальной блокады Великобритании. По условиям Тильзитского мира 1807 года Россия должна была присоединиться к блокаде, но продолжала тайно торговать с Англией, что подрывало её экономику. 
# Стремление Наполеона к господству в Европе. Он видел в России препятствие на пути к мировому господству. 
# Личные противоречия между Наполеоном и Александром I. Например, Наполеон обвинял Александра в убийстве своего отца Павла I, а Александр отказался выдать замуж за Наполеона свою сестру — княжну Анну Павловну. 
# Основные события
# 12 июня 1812 года — начало войны: армия Наполеона переправилась через реку Неман и вторглась в Россию. 
# 4–6 августа 1812 года — битва за Смоленск, русские войска оставили город. 
# 26 августа 1812 года — Бородинское сражение — одно из самых кровопролитных сражений войны. Потери были колоссальными, ни одна из сторон не добилась решающего успеха. 
# 1 сентября 1812 года — совет в Филях, на котором было принято решение оставить Москву. 
# 2 сентября 1812 года — французская армия вошла в пустую Москву, где вскоре начался пожар, уничтоживший большую часть города. 
# 7 октября 1812 года — Наполеон начал отступление из Москвы. Оно превратилось в катастрофу из-за партизанских атак, морозов и голода. 
# 14–17 ноября 1812 года — переправа через реку Березину, где французская армия понесла огромные потери. 
# 25 декабря 1812 года — манифест Александра I об окончании войны. 
# Итоги и значение
# Победа России. Она сохранила независимость страны и подорвала военное могущество наполеоновской Франции, которая потеряла в России свыше 500 тысяч человек, всю кавалерию и почти всю артиллерию. 
# Укрепление международного авторитета России. Страна стала одной из ведущих европейских держав. 
# Рост национального самосознания. В борьбе против захватчиков участвовали все слои общества — от крестьян до дворян. 
# Зарождение общественного движения. Победа над Наполеоном способствовала формированию идеологии декабристов. 
# Экономические потери. Центральные и западные районы Европейской России подверглись разорению, что стало причиной затяжного экономического кризиса. 
# Отечественная война 1812 года оставила значительный след в культуре, искусстве и исторической памяти. Ей посвящены литературные произведения (например, «Война и мир» Л. Н. Толстого, «Бородино» М. Ю. Лермонтова), фильмы и памятники.''')

# new_topic(subject_id=3, title='первая мировая война', theory='''Первая мировая война (1914–1918) стала одним из самых масштабных и разрушительных конфликтов в истории человечества. В неё были вовлечены 38 государств, а боевые действия охватили Европу, Азию и Африку. Поводом к войне послужило убийство эрцгерцога Франца Фердинанда, но истинными причинами стали глубокие противоречия между великими державами — борьба за колонии, рынки сбыта и сферы влияния.
# Война принесла невиданные ранее страдания: миллионы погибших, появление новых видов оружия (танки, отравляющие газы, авиация) и крушение четырёх империй — Российской, Германской, Австро-Венгерской и Османской. Она изменила ход истории, положив начало революциям, распаду старых монархий и созданию новых государств. Однако жестокий Версальский мир, завершивший войну, заложил мины замедленного действия, которые спустя два десятилетия привели ко Второй мировой войне. Память о Первой мировой — это напоминание о том, какой ценой обходится человечеству стремление к переделу мира.''')

# new_topic(subject_id=3, title='ВОВ', theory='''Великая Отечественная война (1941–1945) — важнейшая и решающая часть Второй мировой войны, в которой Советский Союз сражался против нацистской Германии и её союзников. Начавшись 22 июня 1941 года с вероломного вторжения армий вермахта, эта война стала величайшим испытанием для всего советского народа.
# Ключевыми событиями стали героическая оборона Брестской крепости, битва за Москву, где был развеян миф о непобедимости врага, сталинградская и курская битвы, ознаменовавшие коренной перелом. Итогом войны стал разгром гитлеровских войск, освобождение народов Европы и взятие Берлина в мае 1945 года.
# Победа досталась невероятно высокой ценой — более 27 миллионов человеческих жизней, тысячи разрушенных городов и сёл. Эта война навсегда останется в истории как символ беспримерного мужества, стойкости и единства людей, отстоявших свою Родину и свободу.''')

# new_test(topics_id=2, question='Сколько государств было вовлечено в Первую мировую войну?', answer='38 государств')
# new_test(topics_id=2, question='Какое событие стало поводом к началу войны?', answer='Убийство эрцгерцога Франца Фердинанда')
# new_test(topics_id=2, question='Какие четыре империи рухнули в результате войны?', answer='Российская, Германская, Австро-Венгерская и Османская')
# new_user_result()

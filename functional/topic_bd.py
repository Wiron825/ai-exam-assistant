from start_bd import *

def look_subject_in_topic():
    with engine.begin() as conn:
        data = conn.execute(text("SELECT subject_id FROM topics"))
        data = [i for row in data for i in row]
        print(data)
    return data


def look_topic_questions(subject_id):
    if subject_id not in look_subject_in_topic():
        print('Ошибка')
        return False

    with Session(engine) as session:
        sql = text('''
            SELECT title
            FROM topics
            WHERE subject_id = :subject_id
            ''')
        result = session.execute(sql, {"subject_id": subject_id}).scalars().all()
        print(result)
    return result


def look_topic_theory(subject_id):
    if subject_id not in look_subject_in_topic():
        print('Ошибка')
        return False

    with Session(engine) as session:
        sql = text('''
            SELECT theory
            FROM topics
            WHERE subject_id = :subject_id
            ''')
        result = session.execute(sql, {"subject_id": subject_id}).scalar()
        print(result)
    return result


def look_topic_id(subject_id, title):
    if subject_id not in look_subject_in_topic():
        print('Ошибка')
        return False

    with Session(engine) as session:
        sql = text('''
            SELECT id
            FROM topics
            WHERE subject_id = :subject_id
            AND title = :title
            ''')
        result = session.execute(sql, {"subject_id": subject_id, "title": title}).scalar()
        print(result)
    return result

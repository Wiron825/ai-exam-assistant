from start_bd import *

def look_id_in_topic():
    with engine.begin() as conn:
        data = conn.execute(text("SELECT topics_id FROM tests"))
        data = [i for row in data for i in row]
        print(data)
    return data


def look_questions_in_test(topic_id):
    if topic_id not in look_id_in_topic():
        print('Ошибка')
        return False

    with Session(engine) as session:
        sql = text('''
            SELECT question
            FROM tests
            WHERE topics_id = :topic_id
            ''')
        result1 = session.execute(sql, {"topic_id": topic_id}).scalars().all()

        sql = text('''
            SELECT answer
            FROM tests
            WHERE topics_id = :topic_id
            ''')
        result2 = session.execute(sql, {"topic_id": topic_id}).scalars().all()
        result = {result1[i]: result2[i] for i in range(len(result1))}
        print(result)
    return result


def look_answer_in_test(question):
    with Session(engine) as session:
        sql = text('''
            SELECT answer
            FROM tests
            WHERE question = :question
            ''')
        result = session.execute(sql, {"question": question}).scalar()
        print(result)
    return result

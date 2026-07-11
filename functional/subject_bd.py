from start_bd import *

def look_subject():
    with engine.begin() as conn:
        data = conn.execute(text("SELECT subject FROM subjects"))
        data = [i for row in data for i in row]
        print(data)
    return data


def look_id_subject(subject):
    with Session(engine) as session:
        sql = text('''
            SELECT id
            FROM subjects
            WHERE subject = :subject
            ''')
        result = session.execute(sql, {"subject": subject}).scalar()
        print(result)
    return result


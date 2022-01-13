import pymysql


def show_table(name):
    try:
        conn = pymysql.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="642479",
            db="user",
        )
        cursor = conn.cursor()
        # show_sql = "select * from student"
        show_sql = "select * from student where name =%(name)s "
        # print(show_sql)
        rows_affected = cursor.execute(show_sql, {"name": name})
        rows = cursor.fetchall()
        rows_1 = cursor.fetchone()
        print(rows_1)
        str_name = "小飞"
        for row in rows:
            if str_name in row:
                print(str_name)
            print(row)

    except Exception as e:
        print(f"search mysql with err: {e}")
    finally:
        cursor.close()
        conn.close()
    return rows

def insert_name(name):
    try:
        conn = pymysql.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="642479",
            db="user",
        )
        cursor = conn.cursor()
        show_sql = "insert into student(name,age, sex) values (%s, %s, %s)"
        values = (name, 18, "男")
        cursor.execute(show_sql, values)
        conn.commit()
    except Exception as e:
        print(f"search mysql with err: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    rows = show_table("小明")
    rows_1 = insert_name("小云")
    rows =show_table("小云")
    print(rows)

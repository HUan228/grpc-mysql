# coding=utf-8
from concurrent import futures

import grpc
import pymysql

import test_pb2
import test_pb2_grpc
from test_pb2 import User


class UserService(test_pb2_grpc.UserStorageServicer):
    def get_conn(self):
        conn = pymysql.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="642479",
            db="user",
        )
        return conn

    def show_tables(self, name):
        try:
            conn = self.get_conn()
            cursor = conn.cursor()
            show_sql = "select * from student where name =%(name)s;"
            cursor.execute(show_sql, {"name": name})
            rows = cursor.fetchall()
            stu_list = []
            for row in rows:
                print(row)
                stu_list.append(
                    User(
                        stu_name=row[0],
                        stu_id=row[1],
                        stu_age=row[2],
                        stu_sex=row[3]
                    )
                )
            print(stu_list)
            return stu_list

        except Exception as e:
            print(f"search mysql with err: {e}")
        finally:
            cursor.close()
            conn.close()

    def insert_name(self, name, id, age, sex):
        try:
            conn = self.get_conn()
            cursor = conn.cursor()
            show_sql = "insert into student(name, id, age, sex) values (%s, %s, %s, %s)"
            values = (name, id, age, sex)
            cursor.execute(show_sql, values)
            conn.commit()
        except Exception as e:
            print(f"search mysql with err: {e}")
        finally:
            cursor.close()
            conn.close()

    def delete_name(self, name):
        try:
            conn = self.get_conn()
            cursor = conn.cursor()
            sql = "delete from student where name = %s;"
            cursor.execute(sql, name)
            conn.commit()
        except Exception as e:
            print("error is ", e)
        finally:
            cursor.close()
            conn.close()

    def update_table(self, id):
        try:
            conn = self.get_conn()
            cursor = conn.cursor()
            sql = "update student set name='小白' where id=%s;"
            cursor.execute(sql, id)
            conn.commit()
        except Exception as e:
            print("error is ", e)
        finally:
            cursor.close()
            conn.close()




    def QueryUserInfo(self, request, context):
        name = request.cond.stu_name
        students = self.show_tables(name)
        print("User server transer: ", students)
        return test_pb2.QueryReply(user_list=students)

    def InsertUser(self, request, context):
        name = request.cond.stu_name
        id = request.cond.stu_id
        age = request.cond.stu_age
        sex = request.cond.stu_sex
        self.insert_name(name, id, age, sex)
        print("transer")
        return test_pb2.CommonReply(code=200, message="success")


    def DeleteUser(self, request, context):
        name = request.cond.stu_name
        self.delete_name(name)
        print("delete...")
        return test_pb2.CommonReply(code=200, message="success")

    def UpdateUser(self, request, context):
        id = request.cond.stu_id
        self.update_table(id)
        print("update....")
        return test_pb2.CommonReply(code=200, message="success")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    test_pb2_grpc.add_UserStorageServicer_to_server(UserService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()

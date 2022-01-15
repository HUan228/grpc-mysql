# coding=utf-8
from concurrent import futures

import asyncio
import grpc
import pymysql

import test_pb2
import test_pb2_grpc
from test_pb2 import User
from aiohttp import web
from grpc.experimental.aio import init_grpc_aio
from test_pb2_grpc import add_UserStorageServicer_to_server
from test_pb2_grpc import UserStorageServicer


class HelloWorldview(web.View):
    async def get(self):
        return web.Response(text="Hello World!")



class Application(web.Application):
    def __init__(self):
        super().__init__()

        self.grpc_task = None
        self.grpc_server = GrpcServer()

        self.add_routes()
        self.on_startup.append(self.__on_startup())
        self.on_shutdown.append(self.__on_shutdown())

    def __on_startup(self):
        async def _on_startup(app):
            self.grpc_task = \
                asyncio.ensure_future(app.grpc_server.start())
        return _on_startup

    def __on_shutdown(self):
        async def _on_shutdown(app):
            await app.grpc_server.stop()
            app.grpc_task.cancel()
            await app.grpc_task
        return _on_shutdown

    def add_routes(self):
        self.router.add_view('/helloworld', HelloWorldview)

    def run(self):
        return web.run_app(self, port=8000)

class UserService(UserStorageServicer):
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


class GrpcServer:
    def __init__(self):
        print("init grpc server")
        init_grpc_aio()
        #self.server = grpc.experimental.aio.server()
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        self.servicer = UserService()
        add_UserStorageServicer_to_server(
            self.servicer,
            self.server)

        self.server.add_insecure_port("[::]:50051")
        print("init sucess")

    async def start(self):
        print("start grpc service...")
        await self.server.start()
        await self.server.wait_for_termination()

    async def stop(self):
        await self.server.close()
        await self.server.wait_for_termination()

application = Application()


if __name__ == '__main__':
    application.run()

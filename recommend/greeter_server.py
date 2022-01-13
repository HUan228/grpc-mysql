from concurrent import futures

import logging
import grpc
import helloworld_pb2
import helloworld_pb2_grpc


###
# user_info: id, name, age, sex
# message User{id, name, age, sex}
# QueryUserInfo(User) (User)  sql: select id, name, age, sex from table_name where id = '{}';
# InsertUser(User) (Reply)    sql:
# DeleteUser(User) (Reply)    sql:
# UpdateUser(User) (Reply)    sql:

###

class Greeter(helloworld_pb2_grpc.GreeterServicer):

    def SayHello(self, request, context):
        print("Greeter server receive{}".format(request.name))
        return helloworld_pb2.HelloReply(message='Hello, %s!' % request.name)
    def SayHelloAgain(self, request, context):
        return helloworld_pb2.HelloReply(message='Hello again, %s' % request.name)
    def Test(self, request, context):
        return helloworld_pb2.HelloReply(message='Test, %s' % request.name)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
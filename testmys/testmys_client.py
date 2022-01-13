#-*-coding:utf-8-*
import asyncio
import json
import logging

import grpc
import test_pb2_grpc
import test_pb2

async def run() -> None:
    async with grpc.aio.insecure_channel('localhost:50051') as channel:
        stub = test_pb2_grpc.UserStorageStub(channel)
        cond_query = test_pb2.User(stu_name="小明")
        response = await stub.QueryUserInfo(test_pb2.CommonRequest(cond=cond_query))
        print(response)
        cond_insert = test_pb2.User(stu_name="小美", stu_id=4, stu_age=18, stu_sex="女")
        response = await stub.InsertUser(test_pb2.CommonRequest(cond=cond_insert))
        print(response)
        cond_delete = test_pb2.User(stu_name="小美")
        response = await stub.DeleteUser(test_pb2.CommonRequest(cond=cond_delete))
        print(response)
        cond_update = test_pb2.User(stu_id=1)
        response = await stub.UpdateUser(test_pb2.CommonRequest(cond=cond_update))
        print(response)


if __name__ == '__main__':
    logging.basicConfig()
    asyncio.run(run())
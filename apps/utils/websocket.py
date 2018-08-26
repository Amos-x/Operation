# from bottle import get, run
# from bottle_websocket import  websocket
# from bottle_websocket import GeventWebSocketServer
#
# users = set()   # 连接进来的websocket客户端集合
# @get('/websocket/', apply=[websocket])
# def chat(ws):
#     users.add(ws)
#     while True:
#         msg = ws.receive()  # 接客户端的消息
#         if msg:
#             for u in users:
#                 u.send(msg) # 发送信息给所有的客户端
#         else:
#             break
#     # 如果有客户端断开连接，则踢出users集合
#     users.remove(ws)
# run(host='0.0.0.0', port=8888, server=GeventWebSocketServer)

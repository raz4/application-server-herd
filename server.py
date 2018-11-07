import socket
import asyncio
import aiohttp
import json
import sys
import re
import time
import decimal

class EchoClientProtocol(asyncio.Protocol):
    def __init__(self, message, loop):
        self.message = message
        self.loop = loop
    
    def connection_made(self, transport):
        transport.write(self.message.encode())
        print("SENT, " + PORT_SERVER_MAP[transport.get_extra_info('peername')[1]] + ": " + self.message)
        print("SENT, " + PORT_SERVER_MAP[transport.get_extra_info('peername')[1]] + ": " + self.message, file=text_file)
    
    def data_received(self, data):
        print('Data received: {!r}'.format(data.decode()))

class EchoServerClientProtocol(asyncio.Protocol):
    async def get_json(self, client, info_bound, url):
        async with client.get(url) as response:
            return await response.json()

    async def get_google_places(self, message, lat, lng, radius, info_bound, client):
        data = await self.get_json(client, info_bound, "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + lat + "," + lng + "&radius=" + str(radius) + "&key=AIzaSyAVAiZjmFvbvEc3Q6UHjDJ9sEaEyjDoILI")
        data = '\n' + json.dumps(data, indent=4, sort_keys=True)
        data = data.encode()
        self.transport.write(message)
        self.transport.write(data)
        print("SENT, Client: Google Data")
        print("SENT, Client: Google Data",file=text_file)
        self.transport.close()

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        print('Connection from {}'.format(peername),file=text_file)
        self.transport = transport

    def shutdown(self, *args):
        self.transport.close()

    def data_received(self, data):
        time_r = time.time()
        
        message_a = data.decode('unicode_escape')
            
        message = message_a.split(" ")
        src_server = ""
        if message[0] in SERVER_PORT_MAP:
            msg_src_server = message[0]
            src_server = ""
            src_port = SERVER_PORT_MAP[message[0]]
            if src_port == port_client_1:
                src_server = PORT_SERVER_MAP[port_client_1]
            elif src_port == port_drop_1:
                src_server = PORT_SERVER_MAP[port_client_1]
            elif src_port == port_client_2:
                src_server = PORT_SERVER_MAP[port_client_2]
            elif src_port == port_drop_2:
                src_server = PORT_SERVER_MAP[port_client_2]
            message = message[1:]
            print("RECEIVED, " + src_server + ": " + message_a)
            print("RECEIVED, " + src_server + ": " + message_a,file=text_file)
            time_stamp = message[3]
            if message[2] in d:
                if d[message[2]][2] > message[4]:
                    print("IAMAT: Ignoring old data...")
                    print("IAMAT: Ignoring old data...",file=text_file)
                    time_stamp = d[message[2]][2]
                else:
                    d[message[2]] = [msg_src_server, message[3], message[4], message[0]]
            else:
                d[message[2]] = [msg_src_server, message[3], message[4], message[0]]
            
            if int(SERVER_PORT_MAP[msg_src_server]) != port_drop_1:
                if int(SERVER_PORT_MAP[msg_src_server]) != port_drop_2:
                    send_port = port_client_1
                    if SERVER_PORT_MAP[msg_src_server] == port_client_1:
                        send_port = port_client_2
                    loop5 = asyncio.get_event_loop()
                    coro5 = loop5.create_connection(lambda: EchoClientProtocol(message_a, loop5), '127.0.0.1', send_port)
                    fut5 = asyncio.ensure_future(coro5)
                    self.transport.close()
        elif message_a.startswith("IAMAT "):
            print("RECEIVED, Client: " + message_a)
            print("RECEIVED, Client: " + message_a, file=text_file)
            if len(message) != 4:
                print("ERROR: Incorrect IAMAT Format")
                print("ERROR: Incorrect IAMAT Format",file=text_file)
                msg = "? " + message_a
                send_data = msg.encode()
                self.transport.write(send_data)
                self.transport.close()
                return
            try:
                time_diff = time_r - float(message[3])
            except:
                print("ERROR: Incorrect IAMAT Format")
                print("ERROR: Incorrect IAMAT Format",file=text_file)
                msg = "? " + message_a
                send_data = msg.encode()
                self.transport.write(send_data)
                self.transport.close()
                return

            try:
                coord = message[2]
                coord_list = re.split('[+-]', coord)
                lat = coord[0] + coord_list[1]
                if coord[0] != '-':
                    if coord[0] != '+':
                        print("ERROR: Incorrect IAMAT Format")
                        print("ERROR: Incorrect IAMAT Format",file=text_file)
                        msg = "? " + message_a
                        send_data = msg.encode()
                        self.transport.write(send_data)
                        self.transport.close()
                        return
                s_message = coord[1:len(coord)]
                second_sign = '-'
                if s_message.find('-') == -1:
                    second_sign = '+'
                    if s_message.find('+') == -1:
                        print("ERROR: Incorrect IAMAT Format")
                        print("ERROR: Incorrect IAMAT Format",file=text_file)
                        msg = "? " + message_a
                        send_data = msg.encode()
                        self.transport.write(send_data)
                        self.transport.close()
                        return
                lng = second_sign + coord_list[2]
            except:
                print("ERROR: Incorrect IAMAT Format")
                print("ERROR: Incorrect IAMAT Format",file=text_file)
                msg = "? " + message_a
                send_data = msg.encode()
                self.transport.write(send_data)
                self.transport.close()
                return

            d_lat = decimal.Decimal(lat)
            if d_lat.as_tuple().exponent > -6:
                print("ERROR: Incorrect IAMAT Format")
                print("ERROR: Incorrect IAMAT Format",file=text_file)
                msg = "? " + message_a
                send_data = msg.encode()
                self.transport.write(send_data)
                self.transport.close()
                return
            d_lng = decimal.Decimal(lng)
            if d_lng.as_tuple().exponent > -6:
                print("ERROR: Incorrect IAMAT Format")
                print("ERROR: Incorrect IAMAT Format",file=text_file)
                msg = "? " + message_a
                send_data = msg.encode()
                self.transport.write(send_data)
                self.transport.close()
                return

            if float(message[3]) < 0:
                print("ERROR: Incorrect IAMAT Format")
                print("ERROR: Incorrect IAMAT Format",file=text_file)
                msg = "? " + message_a
                send_data = msg.encode()
                self.transport.write(send_data)
                self.transport.close()
                return

            sign = '+'
            if time_diff < 0:
                sign = '-'
            time_diff = sign + str(time_diff)
            time_stamp = message[3]
            if message[1] in d:
                if d[message[1]][2] > message[3]:
                    print("IAMAT: Ignoring old data...")
                    print("IAMAT: Ignoring old data...",file=text_file)
                    time_stamp = d[message[1]][2]
                    time_diff = d[message[1]][3]
                else:
                    d[message[1]] = [sys.argv[1], message[2], message[3], time_diff]
            else:
                d[message[1]] = [sys.argv[1], message[2], message[3], time_diff]
            send_data = "AT " + sys.argv[1] + " " + time_diff + " " + message[1] + " " + message[2] + " " + message[3]
            print("SENT, Client: " + send_data)
            print("SENT, Client: " + send_data,file=text_file)
            send_data_2 = send_data.encode()
            self.transport.write(send_data_2)

            loop3 = asyncio.get_event_loop()
            coro3 = loop3.create_connection(lambda: EchoClientProtocol(sys.argv[1] + " "  +str(time_diff) + " " + message_a, loop3), '127.0.0.1', port_client_1)
            fut3 = asyncio.ensure_future(coro3)
            
            loop4 = asyncio.get_event_loop()
            coro4 = loop4.create_connection(lambda: EchoClientProtocol(sys.argv[1] + " " + str(time_diff) + " " + message_a, loop4), '127.0.0.1', port_client_2)
            fut4 = asyncio.ensure_future(coro4)

            self.transport.close()
        elif message_a.startswith("WHATSAT "):
            print("RECEIVED, Client: " + message_a)
            print("RECEIVED, Client: " + message_a,file=text_file)
            if len(message) != 4:
                print("ERROR: Incorrect WHATSAT Format")
                print("ERROR: Incorrect WHATSAT Format",file=text_file)
                msg = "? " + message_a
                send_data = msg.encode()
                self.transport.write(send_data)
                self.transport.close()
                return
            try:
                if int(message[2]) > 50:
                    msg = "? " + message_a
                    send_data = msg.encode()
                    self.transport.write(send_data)
                    self.transport.close()
                    return
                if int(message[3]) > 20:
                    msg = "? " + message_a
                    send_data = msg.encode()
                    self.transport.write(send_data)
                    self.transport.close()
                    return
                if int(message[2]) < 0:
                    msg = "? " + message_a
                    send_data = msg.encode()
                    self.transport.write(send_data)
                    self.transport.close()
                    return
                if int(message[3]) < 0:
                    msg = "? " + message_a
                    send_data = msg.encode()
                    self.transport.write(send_data)
                    self.transport.close()
                    return
            except:
                msg = "? " + message_a
                send_data = msg.encode()
                self.transport.write(send_data)
                self.transport.close()
                return
            time_diff = time_r - float(message[3])
            sign = '+'
            if time_diff < 0:
                sign = '-'
            time_diff = sign + str(time_diff)
            if message[1] in d:
                coord = d[message[1]][1]
                coord_list = re.split('[+-]', coord)
                lat = coord[0] + coord_list[1]
                s_message = coord[1:len(coord)]
                second_sign = '-'
                if s_message.find('-') == -1:
                    second_sign = '+'
                lng = second_sign + coord_list[2]
                send_data = "AT " + d[message[1]][0] + " " + d[message[1]][3] + " " + message[1] + " " + d[message[1]][1] + " " + d[message[1]][2]
                send_data = send_data.encode()
                asyncio.ensure_future(self.get_google_places(send_data, lat, lng, message[2], message[3], client))
        else:
             print("SENT, Client: ? " + message_a)
             print("SENT, Client: ? " + message_a,file=text_file)
             
             msg = "? " + message_a
             send_data = msg.encode()
             self.transport.write(send_data)
             self.transport.close()

PORT_SERVER_MAP = {15200: 'Alford', 15201: 'Ball', 15202: 'Hamilton', 15203: 'Holiday', 15204: 'Welsh'}
SERVER_PORT_MAP = {'Alford': 15200 ,'Ball': 15201 ,'Hamilton': 15202 ,'Holiday': 15203 ,'Welsh': 15204}

d = {}

loop = asyncio.get_event_loop()
loop_server = asyncio.get_event_loop()
client = aiohttp.ClientSession(loop=loop)

port_server = 0
port_client_1 = 0
port_client_2 = 0
port_drop_1 = 0
port_drop_2 = 0
if sys.argv[1] == "Alford":
    port_server = 15200
    port_client_1 = 15202
    port_client_2 = 15204
    port_drop_1 = 15203
    port_drop_2 = 15201
elif sys.argv[1] == "Ball":
    port_server = 15201
    port_client_1 = 15203
    port_client_2 = 15204
    port_drop_1 = 15202
    port_drop_2 = 15200
elif sys.argv[1] == "Hamilton":
    port_server = 15202
    port_client_1 = 15200
    port_client_2 = 15203
    port_drop_1 = 15204
    port_drop_2 = 15201
elif sys.argv[1] == "Holiday":
    port_server = 15203
    port_client_1 = 15201
    port_client_2 = 15202
    port_drop_1 = 15204
    port_drop_2 = 15200
elif sys.argv[1] == "Welsh":
    port_server = 15204
    port_client_1 = 15200
    port_client_2 = 15201
    port_drop_1 = 15202
    port_drop_2 = 15203

text_file = open(sys.argv[1] + "_log.txt","w+")
coro_server = loop_server.create_server(EchoServerClientProtocol, '127.0.0.1', port_server)
server = loop_server.run_until_complete(coro_server)
print("Server Online: " + sys.argv[1])
print('Serving on {}'.format(server.sockets[0].getsockname()))

loop_server.run_forever()

# Close the server
server.close()
loop_server.run_until_complete(server.wait_closed())
loop_server.close()

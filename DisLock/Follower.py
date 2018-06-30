import _thread
import socket
import sys
import json



clients = []
locks = [{"name":'test1',"client":'-1'},{"name":'test2',"client":'-1'}]
req_msgs = []



def connect_leader(leader_host, leader_port):
    leader_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    leader_socket.connect((leader_host, leader_port))
    leader_socket.sendall(b"NewFollower")
    data = leader_socket.recv(1024).decode().split(":")

    if data[0] == "FollowID":
        follwer_id = int(data[1])

    return leader_socket, follwer_id


def update_all(leader_socket):
    locks= []
    index= 0
    while True:
        tmpstr = "UpdateMap:" + str(index)
        leader_socket.sendall(tmpstr.encode())
        msg = leader_socket.recv(1024).decode().split(":")
        print(msg)
        if msg[0] == "UpdateMap" and msg[1] != "Failed":
            index += 1
            locks.append({'name': msg[1], 'client': msg[2]})
        else:
            break

# relay leader's msg to client
def downstream_thread(leader_socket):
    while True:
        print("locks is "+str(locks))
        data = leader_socket.recv(1024).decode()
        # print "data: ", data
        if not data:
            continue

        msg = data.split(":")
        # print "msg: ", msg
        if msg[0] == "PreemptLock":
            locks.append({'name': msg[1], 'client': msg[2]})
        elif msg[0] == "ReleaseLock":
            locks.remove({'name': msg[1], 'client': msg[2]})

        if len(req_msgs) == 0:
            continue

        req = req_msgs[0].split(":")
        # print "req: ", req, msg == req

        if msg[0] == "Failed":
            c = get_client_conn(req[2])
            if not c:
                print("no such client:", req[2])
                continue
            tmpstr = str(req)+":Failed"
            c.sendall(tmpstr.encode())
            req_msgs.pop(0)

        elif msg == req:
            # print "request success"
            c = get_client_conn(req[2])
            if not c:
                print("no such client:", req[2])
                continue
            tmpstr = str(data)+":Success"
            c.sendall(tmpstr.encode())
            req_msgs.pop(0)


def new_client(conn):
    client_id = follower_id * 10000 + len(clients)
    clients.append({'id': client_id, 'conn': conn})
    return client_id


def get_client_conn(client_id):
    for client in clients:
        # print client['id']
        if client['id'] == int(client_id):
            return client['conn']
    return None


def check_lock(lock):
    for l in locks:
        # print l['name'], l['client']
        if l['name'] == lock:
            return {'result': True, 'client': l['client']}

    return {'result': False}


#  relay clients' msg to leader
def upstream_thread(leader_socket, c):
    client_id = 0
    while True:
        try:
            print("locks is " + str(locks))
            data = c.recv(1024).decode()
            if not data:
                continue
            print("Request: " + str(data))
            msg = data.split(":")

            if msg[0] == "NewClient":
                client_id = new_client(c)
                tmpstr="ClientID: "+str(client_id)
                c.sendall(tmpstr.encode())
                continue

            if msg[0] == "PreemptLock":
                req = "PreemptLock:%s:%d" % (msg[1], client_id)
                req_msgs.append(req)
                tmpstr = str(req)
                leader_socket.sendall(tmpstr.encode())
                continue

            if msg[0] == "ReleaseLock":
                req = "ReleaseLock:%s:%d" % (msg[1], client_id)
                req_msgs.append(req)
                tmpstr = str(req)
                leader_socket.sendall(tmpstr.encode())
                continue

            if msg[0] == "CheckLock":
                ret = check_lock(msg[1])
                if ret['result'] == True:
                    tmpstr = "True:" + str(ret['client'])
                    c.sendall(tmpstr.encode())
                else:
                    c.sendall(b"False")
                continue

        except socket.error:
            print("Socket Error Occured at Client" + str(client_id)+". Releasing it's locks now")
            c.close()
            tmpstr = "mass_release:"+ str(client_id)
            leader_socket.sendall(tmpstr.encode())
            update_all(leader_socket)
            return 0


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("usage: IP self_port leader_port\n")
        sys.exit(1)
    host = socket.gethostname() # self host
    print(str(host))
    myaddr = socket.gethostbyname(host)
    print("Running follower node at " + str(myaddr))
    host_ = sys.argv[1] # leader host
    self_port = int(sys.argv[2])
    leader_port = int(sys.argv[3])

    # connect to leader
    leader_socket, follower_id = connect_leader(host_, leader_port)
    _thread.start_new_thread(downstream_thread, (leader_socket,))
    print("Leader connected, get followerID: %d" % follower_id)

    # bind self socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, self_port))
    s.listen(1)
    update_all(leader_socket)
    while True:
        # accept new connection
        conn, addr = s.accept()
        print("Connected by", addr)
        _thread.start_new_thread(upstream_thread, (leader_socket, conn,))
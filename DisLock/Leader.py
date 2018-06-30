import _thread
import socket
import sys
import time

class Leader:
    followers = []
    locks = []
    connections = []


    def new_follower(self,conn):
        follower_id = len(followers)
        followers.append(
            {'id': follower_id, 'conn': conn})
        return follower_id


    def preempt_lock(lock, client):
        for l in locks:
            if l['name'] == lock:
                return {'result': False}

        locks.append({'name': lock, 'client': client})
        news = ("PreemptLock:%s:%s" % (lock, client))
        return {'result': True, 'news': news}


    def release_lock(lock, client):
        for l in locks:
            print("removing "+str(l['name']))
            if l['name'] == lock and l['client'] == client:
                locks.remove({'name': lock, 'client': client})
                news = ("ReleaseLock:%s:%s" % (lock, client))
                return {'result': True, 'news': news}

        return {'result': False}


    def broadcast_news(news):
        print("boradcast:", news)
        for follower in followers:
            conn = follower['conn']
            conn.sendall(news.encode())


    def get_lock_by_index(index):
        if int(index) >= len(locks):
            return {}
        return locks[int(index)]

    def mass_release(id):
        for l in locks:
            if(l['client']==id):
                release_lock(l['name'],l['client'])
                time.sleep(0.1)
        return {'result': True, 'news': 0}

    def work_thread(c):
        follower_id = -1
        while True:
            print("list is "+str(locks))
            try:
                data = c.recv(1024)


                data = data.decode()
                if not data:
                    continue

                print("Request: " + data)
                msg = data.split(":")

                if msg[0] == "mass_release":
                    mass_release(msg[1])

                if msg[0] == "NewFollower":
                    follower_id = new_follower(c)
                    tmpstr = "FollowID: "+str(follower_id)
                    c.sendall(tmpstr.encode())
                    continue

                if msg[0] == "UpdateMap":
                    lock = get_lock_by_index(msg[1])
                    if not lock:
                        c.sendall(b"Failed")
                        continue
                    tmpstr= "UpdateMap:" + str(lock['name']) + ":"+str(lock['client'])
                    c.sendall(tmpstr.encode())
                    continue

                if msg[0] == "PreemptLock":
                    ret = preempt_lock(msg[1], msg[2])
                    if ret['result']:
                        broadcast_news(ret['news'])
                    else:
                        c.sendall(b"Failed")
                    continue

                if msg[0] == "ReleaseLock":
                    ret = release_lock(msg[1], msg[2])
                    if ret['result']:
                        broadcast_news(ret['news'])
                    else:
                        c.sendall(b"Failed")
                    continue
            except socket.error:
                print("Socket Error Occured at Client" + str(follower_id)+"releasing it's locks")
                c.close()
                return 0


    if __name__ == '__main__':
        if len(sys.argv) < 2:
            print("usage: self_port\n")
            sys.exit(1)

        host = socket.gethostname()
        print(str(host))
        myaddr = socket.gethostbyname(host)
        print("Running leader node at " + str(myaddr))
        port = int(sys.argv[1])
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, port))
        s.listen(8)

        while True:
            # accept new connection
            conn, addr = s.accept()
            print("Connected by", addr)

            connections.append(conn)
            _thread.start_new_thread(work_thread, (conn,))

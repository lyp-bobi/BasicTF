import socket
import sys



follower_socket = None
client_id = 0


def connect_follower(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.sendall(b"NewClient")
    data = s.recv(1024).decode().split(":")
    # print data
    if data[0] == "ClientID":
        return s, int(data[1])
    return None, None


def preempt_lock(lock):
    tmpstr = "PreemptLock:"+ str(lock)
    follower_socket.sendall(tmpstr.encode())
    data = follower_socket.recv(1024).decode().split(":")
    print(data)
    if data[0] == "Failed":
        return "Failed"
    else:
        return "Success"


def release_lock(lock):
    tmpstr = "ReleaseLock:" + str(lock)
    follower_socket.sendall(tmpstr.encode())
    data = follower_socket.recv(1024).decode().split(":")
    print(data)
    if data[0] == "Failed":
        return "Failed"
    else:
        return "Success"


def check_lock(lock):
    tmpstr = "CheckLock:" + str(lock)
    follower_socket.sendall(tmpstr.encode())
    data = follower_socket.recv(1024).decode().split(":")
    # print data
    return data


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("usage: follower_ip follower_port\n")
        sys.exit(1)

    host = socket.gethostname()  # self host
    print(str(host))
    myaddr = socket.gethostbyname(host)
    print("Running client node at " + str(myaddr))
    host_ = sys.argv[1]  # follower's host
    follower_port = int(sys.argv[2])

    # connect to follower
    follower_socket, client_id = connect_follower(host_, follower_port)
    print("Follower connected, get clientID: %s" % client_id)

    while True:
        cmd = input("Client%d: " % client_id).split(" ")
        # print cmd

        if cmd[0] == "preempt":
            if cmd[1] == None:
                print("Wrong command! Try again.")
                continue
            ret = preempt_lock(cmd[1])

        elif cmd[0] == "release":
            if cmd[1] == None:
                print("Wrong command! Try again.")
                continue
            ret = release_lock(cmd[1])

        elif cmd[0] == "check":
            if cmd[1] == None:
                print("Wrong command! Try again.")
                continue
            ret = check_lock(cmd[1])
            if ret[0] == "True":
                print("Result: lockName: %s, ownerID: %s" % (cmd[1], ret[1]))
            else:
                print("Result: lockName: %s, ownerID: none" % (cmd[1]))

        else:
            print("Wrong command! Try again.")

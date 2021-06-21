import socket,cv2, pickle,struct,threading,imutils

# create socket
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip = '65.1.2.62'
port = 1234
s.connect((host_ip,port)) # a tuple

def send_vid():
        vid=cv2.VideoCapture(0)
        while True:
                img,frame = vid.read()
                a = pickle.dumps(frame)
                message = struct.pack("Q",len(a))+a
                s.sendall(message)
                cv2.imshow("You",frame)
                key = cv2.waitKey(1) & 0xFF
                if key ==ord('q'):
                        s.close()

send_vid()

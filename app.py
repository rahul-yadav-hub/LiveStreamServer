from flask import Flask, render_template, Response
import cv2, socket, pickle, struct

# Socket Creation
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

host_ip = ''
port = 1234

# Socket Bind
s.bind((host_ip,port))
# Socket Listen
s.listen()

print("Waiting or clients....")


app = Flask(__name__)

@app.route('/')
def index():
    """Streaming The Local Camera"""
    return render_template('index.html')


def gen():
    conn, addr = s.accept()
    data = b""
    payload_size = struct.calcsize("Q")
    while True:
        while len(data) < payload_size:
            packet = conn.recv(4*1024)
            if not packet: break
            data+=packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q",packed_msg_size)[0]

        while len(data) < msg_size:
            data += conn.recv(4*1024)
        frame_data = data[:msg_size]
        data  = data[msg_size:]
        frame = pickle.loads(frame_data)
        ret, frame = cv2.imencode('.jpg', frame)
        frame = frame.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/stream')
def stream():
    return Response(gen(),mimetype='multipart/x-mixed-replace; boundary=frame')


import socket
import threading
import numpy as np
from io import BytesIO
from PIL import Image
from PyQt5.QtGui import QPixmap


def udp_send(udp_socket, send_msg):

    # udp_socket.sendto(bytes(send_msg, encoding="utf-8"), ("192.168.43.127", 7788))
    udp_socket.sendto(bytes(send_msg, encoding="utf-8"), ("127.0.0.1", 9999))
    print("Send successful")


def udp_rec(udp_socket, size, size_grade, roundness, roundness_grade, color, color_grade, healthy_rot, img_l):

    print("rec_ready")

    while True:

        recv_data = udp_socket.recvfrom(262144)

        __, __, frame_buffer = recv_data[0].partition(b':')
        frame = np.load(BytesIO(frame_buffer))['frame']

        if frame[0, 0, 0] == -1:
            udp_socket.close()
            break

        print('get')

        if frame[0, 6, 0] == 1:
            healthy_state = 'rot'
        else:
            healthy_state = 'healthy'

        size.setText(frame[0, 0, 0].astype(str))
        size_grade.setText(frame[0, 1, 0].astype(str))
        roundness.setText((frame[0, 2, 0]/10 + 80).astype(str))
        roundness_grade.setText(frame[0, 3, 0].astype(str))
        color.setText(frame[0, 4, 0].astype(str))
        color_grade.setText(frame[0, 5, 0].astype(str))
        healthy_rot.setText(healthy_state)

        img = frame[1:, :, :]
        img = Image.fromarray(img)
        img = img.resize([512, 512], Image.ANTIALIAS)
        img.save("/home/jon/Pictures/img_test.jpg")

        pixmap = QPixmap("/home/jon/Pictures/img_test.jpg")
        img_l.setPixmap(pixmap)


def udp_init(size, size_grade, roundness, roundness_grade, color, color_grade, healthy_rot, img_l):

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # local_addr = ('', 7788)
    local_addr = ('', 8888)
    udp_socket.bind(local_addr)

    t_rec = threading.Thread(target=udp_rec, args=(udp_socket, size, size_grade, roundness, roundness_grade,
                                                   color, color_grade, healthy_rot, img_l))
    t_rec.start()

    return udp_socket

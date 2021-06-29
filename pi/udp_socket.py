# -*-coding:utf-8-*-

import socket
import threading
import subprocess
import cv2
import sys
import numpy as np
from io import BytesIO

import main


def udp_send(udp_socket, send_msg):

    send_msg = __pack_frame(send_msg)
    udp_socket.sendto(send_msg, ("127.0.0.1", 8888))
    # udp_socket.sendto(send_msg,("192.168.43.205", 7788))
    print("send successful")


def udp_rec(udp_socket):

    while True:
        
        recv_data = udp_socket.recvfrom(1024)
        recv_msg = recv_data[0].decode('utf-8')

        print(recv_msg)

        if recv_msg == 'disconnect':

            udp_send(udp_socket, np.array([-1, -1, -1]).reshape(3, 1, 1))
            udp_socket.close()

            break

        if recv_msg == 'get':

            # subprocess.run(["raspistill", "-o", "/home/pi/Pictures/imgtest.jpg", "-h", "512", "-w", "512"])
            
            # filename = '/home/pi/Pictures/imgtest.jpg'
            filename = '/home/jon/Graduation_project/pi/imgtest.jpg'

            img = cv2.imread(filename)

            grade = main.main_processing(img)
            udp_send(udp_socket, grade)


def udp_init():

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # local_addr = ('', 7788)
    local_addr = ('', 9999)
    udp_socket.bind(local_addr)

    t_rec = threading.Thread(target=udp_rec, args=(udp_socket,))
    t_rec.start()


def __pack_frame(frame):

    f = BytesIO()
    np.savez(f, frame=frame)

    packet_size = len(f.getvalue())
    header = '{0}:'.format(packet_size)
    header = bytes(header.encode())  # prepend length of array

    out = bytearray()
    out += header

    f.seek(0)
    out += f.read()
    return out


if __name__ == "__main__":

    udp_init()

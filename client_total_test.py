# 그래프 찍기
import matplotlib.pyplot as plt
# chain_main3 = 구동체인, step_chain = 스텝체인
from chain_main3 import chain_main_class
from step_chain import step_chain
# 파이썬 이미지 라이브러리
from PIL import Image
# 파이썬 입출력
import io
import numpy as np
# 소켓을 사용하기 위해서는 socket을 import해야 한다.
import socket
# 파이썬 base64라이브러리 인코딩시 사용
import base64
# json을 위한 임포트
import json
from collections import OrderedDict



# RS 명령이 오면 동작 함수
def RS_Chain():
    clt_data['Type'] = 'RS'           
    if data['Content'] == 'Peak':
        a.peak_plot()
        plt.savefig('rs_peak.png')
        with open("rs_peak.png", "rb") as imageFile:
            rs_peak = base64.b64encode(imageFile.read())
            clt_data['Data'] = rs_peak.decode("utf-8")
    elif data['Content'] == 'Raw':
        a.print_row()
        plt.savefig('rs_raw.png')
        with open("rs_raw.png", "rb") as imageFile:
            rs_raw = base64.b64encode(imageFile.read())
            clt_data['Data'] = rs_raw.decode("utf-8")
    elif data['Content'] == 'bandpass':
        a.print_bandpass()
        plt.savefig('rs_bandpass.png')
        with open("rs_bandpass.png", "rb") as imageFile:
            rs_bandpass = base64.b64encode(imageFile.read())
            clt_data['Data'] = rs_bandpass.decode("utf-8")
    elif data['Content'] == 'Sin':
            clt_data['Data'] = a.cal_sin()

# STEP 명령이 오면 동작 함수
def Step_Chain():
    clt_data['Type'] = 'Step'
    if data["Content"] == "Sin":
        chain.cal_sin()
        clt_data['Data'] = chain.elongation_result[0]
    elif data["Content"] == "Raw":
        chain.show_graph("row")
        with open("GG.png", "rb") as imageFile:
            strd = base64.b64encode(imageFile.read())
            clt_data['Data'] = strd.decode("utf-8")
    elif data["Content"] == "Bandpass":
        chain.show_graph("bandpass")
        with open("GG.png", "rb") as imageFile:
            strd = base64.b64encode(imageFile.read())
            clt_data['Data'] = strd.decode("utf-8")
    elif data["Content"] == "Peak":
        chain.show_graph("peak")
        with open("GG.png", "rb") as imageFile:
            strd = base64.b64encode(imageFile.read())
            clt_data['Data'] = strd.decode("utf-8")
    elif data["Content"] == "Autocorrelate":
        chain.show_graph("autocorrelate") 
        with open("GG.png", "rb") as imageFile:
            strd = base64.b64encode(imageFile.read())
            clt_data['Data'] = strd.decode("utf-8")

#===================================================================
print("실행중...")
#===================================================================
# 스텝체인 작동
print("스텝체인...")
chain = step_chain()
chain.Start()
#===================================================================
# 구동체인 작동
print("구동체인...")
a = chain_main_class()
a.load_data()
a.move_graph()
a.X_trans_time()

#auto_bandpass에 데이터와 검증 주파수 범위, fs를 입력하면 peak_plot까지 자동으로 수행한다.
a.auto_bandpass(a,10000,14000,50000)
print("구동체인 완료.")
#===================================================================


#===================================================================

print("연결 대기 중")

# 로컬은 127.0.0.1의 ip로 접속한다.
print("ip 접속 중")
try:
    HOST = '192.168.0.14'
    print("ip 접속 성공")
except:
    print("ip 접속 실패")

# port는 위 서버에서 설정한 9999로 접속을 한다.
print("포트 접속 중")
try:
    PORT = 9999
    print("포트 접속 성공")
except:
    print("포트 접속 실패")

# 소켓을 만든다.
try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("소켓 생성 성공")
except:
    print("소켓 생성 실패")

# connect함수로 접속을 한다.
try:   
    client_socket.connect((HOST, PORT))# 소켓을 사용하기 위해서는 socket을 import해야 한다.
    print("소켓 연결 성공")
except:
    print("소켓 연결 실패")
else:
    print("gg")

#===================================================================

while(True):
    print("대기중")
    data = client_socket.recv(1024)
    
    # 데이터를 수신한다.
    msg = " "
    msg = data.decode()

    # 받은 데이터 확인용
    print('Received from : ', msg)

    # 문자열을 json으로 변환
    data = json.loads(msg)

    # 보내기 위한 json 생성
    clt_data = OrderedDict()
    clt_data['Name'] = data['Name']
    clt_data['Content'] = data['Content']
    clt_data['Time'] = data['Time']
    clt_data['Comment'] = data['Comment']

    # json의 구동체인 부분을 타입별로 나눠준다.
    if data["Type"] == "RS":
        RS_Chain()
        # json을 스트링으로 바꾼다.
        jsonString = json.dumps(clt_data)
        # 데이터 전송
        client_socket.sendall(jsonString.encode())

    elif data["Type"] == "Step":            
        Step_Chain()
        # json을 스트링으로 바꾼다.
        jsonString = json.dumps(clt_data)
        # 데이터 전송
        client_socket.sendall(jsonString.encode())        
    
    elif data["Type"] == "Stop":
        break

client_socket.close()
from socket import *

clientSock = socket(AF_INET, SOCK_STREAM)
# 127.0.0.1 호스트 주소로 8080 포트번호를 허용

clientSock.connect(('127.0.0.1', 8080))

print('연결 확인 됐습니다.')
clientSock.send('I am a client'.encode('utf-8'))

print('메시지를 전송했습니다.')

data = clientSock.recv(1024)
print('받은 데이터 : ', data.decode('utf-8'))
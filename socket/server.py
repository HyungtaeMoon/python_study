from socket import *

# 서버와 클라이언트가 소켓을 통해 주고받는 과정을 간략하게 정리

# AF: Address Family
# AF_INET: IPv4
# SOCK_SETREAM: 소켓 타입
serverSock = socket(AF_INET, SOCK_STREAM)
# 모든 인터페이스와 연결하기 위해 튜플에서 앞에는 빈 문자열을 사용
# 소켓도 인터페이스이다. 그리고 소켓 인터페이스가 OS 에 명령을 보내면 OS 가 받아서 처리
serverSock.bind(('', 8080))
# 해당 소켓이 총 몇개까지 동시 접속을 허용할 것인지 설정
serverSock.listen(1)

connectionSock, addr = serverSock.accept()

print(str(addr), '에서 접속이 확인되었습니다.')

# 1024 byte 만큼만 가져옴, 만약 그 이상이라면 다시 recv() 를 실행하여 나머지를 가져옴
data = connectionSock.recv(1024)
print('받은 데이터 : ', data.decode('utf-8'))

connectionSock.send('I am a server.'.encode('utf-8'))
print('메시지를 보냈습니다.')

# server.py, client.py 를 순서대로 실행하면 client.py 에서 서버와 송수신을 함
# 현재 listen(1) 을 설정했기 때문에 client 두번째부터는 Connection refused 에러 메시지를 띄우게 됨

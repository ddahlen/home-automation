import paramiko, os

from aiy.board import Board, Led
from aiy.voice.audio import play_wav

SSH_IP = '192.168.1.1'
SSH_USER = 'admin'
SSH_PORT = 2222
CRED_PATH = '/home/pi/scripts/.creds'
COMMAND_ON = 'radio on'
COMMAND_OFF = 'radio off'

def wifi_on(session):
	print('Trying to turn the wifi on')
	try:
		session.exec_command(COMMAND_ON)
	finally:
		session.close()

def wifi_off(session):
	print('Trying to turn the wifi off')
	try:
		session.exec_command(COMMAND_OFF)
	finally:
		session.close()

def connect_to_router():
	print('Trying to connect to router')
	try:
		client = paramiko.SSHClient()
		client.load_system_host_keys()
		client.set_missing_host_key_policy(paramiko.WarningPolicy())
		creds = file_get_contents(CRED_PATH)
		creds = creds.strip()
		client.connect(SSH_IP, SSH_PORT, SSH_USER, creds)
		transport = client.get_transport()
		session = transport.open_session()
	finally:
		return session

def file_get_contents(filename):
	with open(filename) as f:
		return f.read()

def main():
	print('PUSH THE BUTTON!')
	with Board() as board:
		wifi_on(connect_to_router())
		wifistatus = 1
		board.led.brightness = 0.1
		board.led.state = Led.PULSE_SLOW
		while True:
			board.button.wait_for_press()
			if wifistatus == 1:
				wifi_off(connect_to_router())
				board.led.state = Led.OFF
				wifistatus = 0
			else:
				wifi_on(connect_to_router())
				board.led.state = Led.PULSE_SLOW
				wifistatus = 1

if __name__ == '__main__':
	main()

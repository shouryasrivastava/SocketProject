import socket
import threading 
import json

IP = "10.120.70.105"#socket.gethostbyname(socket.gethostname())
PORT = 6677
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"
database = {}
cohorts = {}

def handle_client(conn, addr):
	print(f"[NEW CONNECTIONS] {addr} connected.")

	connected = True
	while connected:
		msg = conn.recv(SIZE).decode(FORMAT)
		tokens = msg.split()
		command = tokens[0]
		
		#command,*argus = msg.split()
		if msg == DISCONNECT_MSG:
			connected = False

		print(f"[{addr}] {msg}")
		#msg = f"Msg received: {msg}"
		if command == "open":
			customer = tokens[1]
			balance = int(tokens[2])
			ipv4_address = tokens[3]
			port_b = int(tokens[4])
			port_p = int(tokens[5])
			#customer, balance, ip_address, port_b, port_p = argus
			if customer in database:
				msg = "FAILURE"
			else:
				database[customer] = (float(balance), ipv4_address, int(port_b), int(port_p))
				msg = "SUCCESS"
		
		elif command == "new-cohort":
			n = int(tokens[2])

			if n < 2 or n > len(database):
				msg = "FAILURE"
			else:
				import random
				cohort = set([customer])
				while len(cohort) < n:
					cohort.add(random.choice(list(database.keys())))
				cohort_info = []
				for c in cohort:
					cohort_info.append((c,) + database[c][1:])
				cohorts[customer] = cohort
				
				msg = f"SUCCESS\n " + "\n".join([f"{c[0]} {c[1]} {c[2]} {c[3]}" for c in cohort_info])
            
		elif command == "delete-cohort":
			if customer not in database:
				msg = "FAILURE"
			elif customer not in cohorts:
				msg = "FAILURE"	
			else:
				cohort = cohorts[customer]
				for c in cohort:
					if c != customer:
						try:
							customer_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
							customer_socket.sendto("delete".encode("utf-8"),(database[c][1],database[c][3]))
						except socket.error:
							pass
				del cohorts[customer]
				msg = "SUCCESS"
		elif command == "deposit":
			amount = float(tokens[1])
			balance += amount
			database[customer] = (balance, ipv4_address, port_b, port_p)
			print(database)
			msg = "SUCCESS"

		elif command == "withdrawal":
			amount = float(tokens[1])
			balance -= amount
			database[customer] = (balance, ipv4_address, port_b, port_p)
			print(database)
			msg = "SUCCESS"
		elif command == "transfer":
			amount = float(tokens[1])
			recipient = tokens[2]
			label = int(tokens[3])
			if customer not in database:
				msg = "FAILURE"
			elif database[customer][0] < amount:
				msg = "FAILURE"
			elif recipient not in database:
				msg = "FAILURE"
			else:
				sender_balance = database[customer][0] - amount
				recipient_balance = database[recipient][0] + amount
				database[customer] = (sender_balance,) + database[customer][1:]
				database[recipient] = (recipient_balance,) + database[recipient][1:]
				msg = "SUCCESS"
    
		elif command == "exit":
			if customer not in database:
				msg = "FAILURE"	
			else:
				del database[customer]
				if customer in cohorts:
					del cohorts[customer]
				msg = "SUCCESS"
		conn.send(msg.encode(FORMAT))


	conn.close()


def main():
	print("[STARTING] Server is starting...")
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind(ADDR)
	server.listen()
	print(f"[LISTENING] Server is listening on {IP}:{PORT}")

	while True:
		conn, addr = server.accept()
		thread = threading.Thread(target=handle_client, args=(conn,addr))
		thread.start()
		#print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


if __name__ == "__main__":
	main()
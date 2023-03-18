import socket


IP = "10.120.70.105"#socket.gethostbyname(socket.gethostname())
PORT = 6677
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"

def main():
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect(ADDR)
	print(f"[CONNECTED] Client connected to server at {IP}:{PORT}")

	connected = True
	while connected:
		msg = input("> ")

		client.send(msg.encode(FORMAT))

		if msg == DISCONNECT_MSG:
			connected = False
		else:
			msg = client.recv(SIZE).decode(FORMAT)
			print(f"[SERVER] {msg}")
		
        # Add handling of transfer and lost-transfer commands
		tokens = msg.split()
		command = tokens[0]


		if command == "transfer":
			amount = float(tokens[1])
			recipient = tokens[2]
			label = int(tokens[3])
			msg = f"transfer {amount} {recipient} {label}"
			client.send(msg.encode(FORMAT))
			response = client.recv(SIZE).decode(FORMAT)
			print(f"[SERVER] {response}")

		#if command == "transfer":
			#amount = float(tokens[1])
			#recipient = tokens[2]
			#label = int(tokens[3])
			#msg = f"transfer {amount} {recipient} {label}"
			#client.send(msg.encode(FORMAT))
			#response = client.recv(SIZE).decode(FORMAT)
			#print(f"[SERVER] {response}")
			#amount, recipient, label = float(tokens[1]), tokens[2], int(tokens[3])
            # Code to perform the transfer operation and update the states
			
			#elif command == "lost-transfer":
			#	amount = float(tokens[1])
			#	recipient = tokens[2]
                # Code to perform the lost-transfer operation and update the states
			#	sender = tokens[-1]
                # Decrement balance at sender and record lost-transfer
			#	database[sender] = (database[sender][0]-amount,) + database[sender][1:]
			#	Cpq = database[sender][3][recipient]
			#	Cpq.append(("lost-transfer", amount))
                # Increment label of outgoing messages to recipient in cohort
			#	for c in cohorts[sender]:
				#	if c != recipient:
 				#		cohorts[sender][c] += 1



if __name__ == "__main__":
	main()
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog

# Client configuration
HOST = '127.0.0.1'
PORT = 12345

class ChatClient:
    def __init__(self, master):
        self.master = master
        self.master.title("Chat Client")

        self.username = simpledialog.askstring("Username", "Please enter your username:", parent=self.master)
        if not self.username:
            self.master.destroy()
            return

        self.chat_window = scrolledtext.ScrolledText(master)
        self.chat_window.pack(padx=20, pady=5)
        self.chat_window.config(state=tk.DISABLED)

        self.message_entry = tk.Entry(master, width=50)
        self.message_entry.pack(padx=20, pady=5)
        self.message_entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.pack(pady=5)

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((HOST, PORT))

        threading.Thread(target=self.receive_messages).start()

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message:
                    self.display_message(message)
            except Exception as e:
                print(f"An error occurred: {e}")
                self.client_socket.close()
                break

    def send_message(self, event=None):
        message = self.message_entry.get()
        self.message_entry.delete(0, tk.END)
        formatted_message = f"{self.username}: {message}"
        self.client_socket.send(formatted_message.encode('utf-8'))
        self.display_message(formatted_message)

    def display_message(self, message):
        self.chat_window.config(state=tk.NORMAL)
        self.chat_window.insert(tk.END, message + '\n')
        self.chat_window.config(state=tk.DISABLED)
        self.chat_window.yview(tk.END)

def start_client():
    root = tk.Tk()
    client = ChatClient(root)
    root.mainloop()

if __name__ == "__main__":
    start_client()

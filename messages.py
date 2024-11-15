import sqlite3
from datetime import datetime


class Message:
    def __init__(self, message_id, sender_id, receiver_id, content, timestamp):
        self.__message_id = message_id
        self.__sender_id = sender_id
        self.__receiver_id = receiver_id
        self.__content = content
        self.__timestamp = timestamp

    @property
    def message_id(self):
        return self.__message_id

    @property
    def sender_id(self):
        return self.__sender_id

    @property
    def receiver_id(self):
        return self.__receiver_id

    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, value):
        self.__content = value

    @property
    def timestamp(self):
        return self.__timestamp

    def __str__(self):
        return f"Sender: {self.sender_id} \nRecipient: {self.receiver_id} \nContent: {self.content} \nTimestamp: {self.timestamp}"

    @classmethod
    def add_message(cls, sender_id, receiver_id, content, timestamp=None):
        timestamp = timestamp or datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO messages (sender_id, receiver_id, content, timestamp)
                              VALUES (?, ?, ?, ?)''', (sender_id, receiver_id, content, timestamp))
            conn.commit()

    @classmethod
    def del_message(cls, message_id):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM messages WHERE message_id=?', (message_id,))
            conn.commit()

    @classmethod
    def edit_message(cls, message_id, content, timestamp):
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''UPDATE messages SET content=?, timestamp=? WHERE message_id=?''',
                           (content, timestamp, message_id))
            conn.commit()

    @classmethod
    def get_all_messages(cls):
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT conversation_id,message_id, sender_id, receiver_id, content, timestamp FROM messages')
            rows = cursor.fetchall()
            return [{'conversation_id': row[0],"message_id": row[1], "sender_id": row[2], "receiver_id": row[3], 
                     "content": row[4], "timestamp": row[5]} for row in rows]


class Conversation:
    def __init__(self, user_id, other_user_id):
        self.user_id = user_id
        self.other_user_id = other_user_id
        self.conversation_id = Conversation.create_conversation(user_id,other_user_id)
        self.messages = Conversation.get_conversation_messages(self.conversation_id)

    @classmethod
    def create_conversation(cls, user_id, other_user_id):
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO conversations (participant1_id, participant2_id, message_ids)
                              VALUES (?, ?, ?)''', (user_id, other_user_id, ''))
            conn.commit()
            return cursor.lastrowid

    @classmethod
    def insert_message(cls, conversation_id, sender_id, receiver_id, content, timestamp=None):
        timestamp = timestamp or datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO messages (conversation_id, sender_id, receiver_id, content, timestamp)
                              VALUES (?, ?, ?, ?, ?)''', (conversation_id, sender_id, receiver_id, content, timestamp))
            message_id = cursor.lastrowid

            cursor.execute('''SELECT message_ids FROM conversations WHERE conversation_id=?''', (conversation_id,))
            current_message_ids = cursor.fetchone()
            new_message_ids = f"{current_message_ids},{message_id}" if current_message_ids else str(message_id)
            cursor.execute('''UPDATE conversations SET message_ids=? WHERE conversation_id=?''',
                           (new_message_ids, conversation_id))
            conn.commit()

    @classmethod
    def get_conversation_messages(cls, conversation_id):
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT message_id, sender_id, receiver_id, content, timestamp, conversation_id
                              FROM messages WHERE conversation_id=? ORDER BY timestamp''', 
                           (conversation_id,))
            msg = cursor.fetchone()
            message_dict = {"message_id": msg[0],
                    "sender_id": msg[1],
                    "receiver_id": msg[2],
                    "content": msg[3],
                    "timestamp": msg[4],
                    'conversation_id':msg[5]}
            return message_dict
        
    @classmethod
    def get_all_conversation_messages(cls, conversation_id):
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT message_id, sender_id, receiver_id, content, timestamp, conversation_id
                              FROM messages WHERE conversation_id=? ORDER BY timestamp''', 
                           (conversation_id,))
            messages = cursor.fetchall()
            message_dict = [{"message_id": msg[0],
                    "sender_id": msg[1],
                    "receiver_id": msg[2],
                    "content": msg[3],
                    "timestamp": msg[4],
                    'conversation_id':msg[5]}for msg in messages]
            return message_dict

    @classmethod
    def get_user_conversations(cls, user_id):
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT conversation_id, participant1_id, participant2_id, message_ids
                              FROM conversations WHERE participant1_id=? OR participant2_id=?''', 
                           (user_id, user_id))
            return cursor.fetchall()


def create_message_table():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
            message_id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id INTEGER NOT NULL,
            sender_id INTEGER NOT NULL,
            receiver_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (conversation_id) REFERENCES conversations(conversation_id),
            FOREIGN KEY (sender_id) REFERENCES users(user_id),
            FOREIGN KEY (receiver_id) REFERENCES users(user_id)
        )''')
        conn.commit()


def create_convo_table():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS conversations (
            conversation_id INTEGER PRIMARY KEY AUTOINCREMENT,
            participant1_id INTEGER NOT NULL,
            participant2_id INTEGER NOT NULL,
            message_ids TEXT,
            FOREIGN KEY (participant1_id) REFERENCES users(user_id),
            FOREIGN KEY (participant2_id) REFERENCES users(user_id)
        )''')
        conn.commit()


if __name__ == '__main__':
   #create_message_table()
   #create_convo_table()
   print(Message.get_all_messages())
   print(Conversation.get_user_conversations(1))
    
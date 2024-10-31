import sqlite3

class Message:
    def __init__(self, message_id, sender_id, receiver_id, content, timestamp):
        self.__message_id = message_id
        self.__sender_id = sender_id
        self.__receiver_id = receiver_id
        self.__content = content
        self.__timestamp = timestamp

    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, value):
        self.__content = value

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
    def timestamp(self):
        return self.__timestamp

    def __str__(self):
        return "Sender: {} \n Recipient: {} \n Content: {} \n Timestamp: {}".format(self.sender_id, self.receiver_id,self.content,self.timestamp)
    
    @classmethod
    def delMessage(cls, message_id):
        conn = None
        conn = sqlite3.connect( "database.db")
        sql='DELETE FROM messages WHERE message_id=?'
        cur = conn.cursor()
        cur.execute(sql, (message_id,))
        conn.commit()
        conn.close()

    @classmethod
    def addMessage(cls, message_id, sender_id, receiver_id, content, timestamp):
        conn = None
        conn = sqlite3.connect( "database.db")
        sql='INSERT INTO users ( message_id, sender_id, receiver_id, content, timestamp) values (?,?,?,?,?)'
        cur = conn.cursor()
        cur.execute(sql, ( message_id, sender_id, receiver_id, content, timestamp,))
        conn.commit()
        if conn:
            conn.close()

    @classmethod
    def editMessage(cls, message_id, content, timestamp):
        conn = None
        conn = sqlite3.connect('database.db')
        sql='UPDATE users SET content=?, timestamp=? WHERE message_id = ?'
        cur = conn.cursor()
        cur.execute(sql, ( content, timestamp, message_id,))
        conn.commit()
        conn.close()

    @classmethod
    def getAllMessages(cls):
        conn = sqlite3.connect('database.db')
        cursorObj = conn.cursor()
        cursorObj.execute('SELECT message_id, sender_id, receiver_id, content, timestamp FROM messages;')
        allRows = cursorObj.fetchall()
        ListOfDictionaries = []
        for row in allRows:
            m = {"message_id": row[0], "sender_id":row[1], 'receiver_id': row[2], 'content':row[3], 'timestamp':row[4]}
            ListOfDictionaries.append(m)
        if conn:
            conn.close()
        return ListOfDictionaries
    
    

def InsertStartingData():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    message_data = [
        (1, 2, 1, 'Is the radio still available?', '2023-01-13 10:15 AM'),
        (2, 1, 2, 'I''m interested in the gardening tools!', '2023-01-14 02:20 PM')]
    cur.executemany('''INSERT INTO messages (message_id, sender_id, receiver_id, content, timestamp) VALUES (?, ?, ?, ?, ?)''', message_data)
    conn.commit()
    conn.close()

def createMessageTable():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE messages (message_id INTEGER PRIMARY KEY AUTOINCREMENT,sender_id INTEGER,receiver_id INTEGER,content TEXT NOT NULL,timestamp TEXT NOT NULL,FOREIGN KEY (sender_id) REFERENCES Users(user_id),FOREIGN KEY (receiver_id) REFERENCES Users(user_id));''')
    conn.commit()
    conn.close()


if __name__ == '__main__':
    createMessageTable()
    InsertStartingData()
    print(Message.getAllMessages())
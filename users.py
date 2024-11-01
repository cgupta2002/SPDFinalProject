import sqlite3

class User:
    def __init__(self, user_id, username, name, email, password, profile_image, location):
        self.__userID = user_id
        self.__username = username
        self.__name = name
        self.__email = email
        self.__password = password
        self.__profile_image = profile_image
        self.__location = location
   
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        self.__email = value

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value):
        self.__password = value
    
    @property
    def profile_image(self):
        return self.__profile_image

    @profile_image.setter
    def profile_image(self, value):
        self.__profile_image = value

    @property
    def location(self):
        return self.__location

    @location.setter
    def location(self, value):
        self.__location = value

    @property
    def username(self):
        return self.__username
    
    @username.setter
    def username(self,value):
        self.__username = value

    def __str__(self):
        return "Username: {} \n Name: {} \n Email: {} \n Location: {} ".format(self.username, self.name,self.email,self.location)
    
    @classmethod
    def delUser(cls, user_id):
        conn = None
        conn = sqlite3.connect( "database.db")
        sql='DELETE FROM users WHERE user_id=?'
        cur = conn.cursor()
        cur.execute(sql, (user_id,))
        conn.commit()
        conn.close()

    @classmethod
    def addUser(cls, user_id, username, name, email, password, profile_image, location):
        conn = None
        conn = sqlite3.connect( "database.db")
        sql='INSERT INTO users ( user_id,username, name, email, password, profile_image, location) values (?,?,?,?,?,?,?)'
        cur = conn.cursor()
        cur.execute(sql, ( user_id, username,name, email, password, profile_image, location,))
        conn.commit()
        if conn:
            conn.close()

    @classmethod
    def updateUser(cls,  user_id, username, name, email, password, profile_image, location):
        conn = None
        conn = sqlite3.connect('database.db')
        sql='UPDATE users SET username=?, name=?, email=?, password=?, profile_image=?, location = ? WHERE user_id = ?'
        cur = conn.cursor()
        cur.execute(sql, (username, name, email, password, profile_image, location, user_id,))
        conn.commit()
        conn.close()

    @classmethod
    def getAllUsers(cls):
        conn = sqlite3.connect('database.db')
        cursorObj = conn.cursor()
        cursorObj.execute('SELECT user_id, username, name, email, password, profile_image, location FROM users;')
        allRows = cursorObj.fetchall()
        ListOfDictionaries = []
        for row in allRows:
            m = {"user_id": row[0], 'username':row[1],"name":row[2], 'email': row[3], 'password':row[4], 'profile_image':row[5], 'location':row[6]}
            ListOfDictionaries.append(m)
        if conn:
            conn.close()
        return ListOfDictionaries
    
    def getUser(username):
        conn = sqlite3.connect('database.db')
        cursorObj = conn.cursor()
        sql='SELECT user_id, username, password FROM users WHERE username=?'
        cursorObj.execute(sql, (username,))
        user = cursorObj.fetchone()
        conn.close()
        return user
    
    def getUserByID(cls,user_id):
        conn = sqlite3.connect('database.db')
        cursorObj = conn.cursor()
        sql='SELECT user_id, username, password FROM users WHERE user_id=?'
        cursorObj.execute(sql, (user_id,))
        user = cursorObj.fetchone()
        conn.close()
        return user
    

def InsertStartingData():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    user_data = [
        (1, 'jdoe123','John Doe', 'johndoe@example.com', 'hashed_password_1', '/images/johndoe.jpg', 'New York, NY'),
        (2, 'jsmith2030','Jane Smith', 'janesmith@example.com', 'hashed_password_2', '/images/janesmith.jpg', 'Los Angeles, CA')]
    cur.executemany('''INSERT INTO Users (user_id, username, name, email, password, profile_image, location) VALUES (?, ?, ?, ?, ?, ?, ?)''', user_data)
    conn.commit()
    conn.close()

def createUserTable():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE Users (user_id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT NOT NULL, name TEXT NOT NULL,email TEXT NOT NULL UNIQUE,password TEXT NOT NULL,profile_image TEXT,location TEXT);''')
    conn.commit()
    conn.close()


if __name__ == '__main__':
    createUserTable()
    InsertStartingData()
    print(User.getAllUsers())
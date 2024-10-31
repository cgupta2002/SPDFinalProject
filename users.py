import sqlite3

class User:
    def __init__(self, user_id, name, email, password, profile_image, location):
        self.__userID = user_id
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

    def __str__(self):
        return "Resource Title: {} \n Description: {} \n Category: {} \n Availability: {} \n Date Posted: {}".format(self.title, self.description,self.category,self.availability,self.datePosted)
    
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
    def addUser(cls, user_id, name, email, password, profile_image, location):
        conn = None
        conn = sqlite3.connect( "database.db")
        sql='INSERT INTO users ( user_id, name, email, password, profile_image, location) values (?,?,?,?,?,?)'
        cur = conn.cursor()
        cur.execute(sql, ( user_id, name, email, password, profile_image, location ))
        conn.commit()
        if conn:
            conn.close()

    @classmethod
    def updateUser(cls,  user_id, name, email, password, profile_image, location):
        conn = None
        conn = sqlite3.connect('database.db')
        sql='UPDATE users SET name=?, email=?, password=?, profile_image=?, location = ? WHERE user_id = ?'
        cur = conn.cursor()
        cur.execute(sql, (name, email, password, profile_image, location, user_id))
        conn.commit()
        conn.close()

    @classmethod
    def getAllUsers(cls):
        conn = sqlite3.connect('database.db')
        cursorObj = conn.cursor()
        cursorObj.execute('SELECT user_id, name, email, password, profile_image, location FROM users;')
        allRows = cursorObj.fetchall()
        ListOfDictionaries = []
        for row in allRows:
            m = {"user_id": row[0], "name":row[1], 'email': row[2], 'password':row[3], 'profile_image':row[4], 'location':row[5]}
            ListOfDictionaries.append(m)
        if conn:
            conn.close()
        return ListOfDictionaries
    
    

def InsertStartingData():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    user_data = [
        (1, 'John Doe', 'johndoe@example.com', 'hashed_password_1', '/images/johndoe.jpg', 'New York, NY'),
        (2, 'Jane Smith', 'janesmith@example.com', 'hashed_password_2', '/images/janesmith.jpg', 'Los Angeles, CA')]
    cur.executemany('''INSERT INTO Users (user_id, name, email, password, profile_image, location) VALUES (?, ?, ?, ?, ?, ?)''', user_data)
    conn.commit()
    conn.close()

def createUserTable():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE Users (user_id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,email TEXT NOT NULL UNIQUE,password TEXT NOT NULL,profile_image TEXT,location TEXT);''')
    conn.commit()
    conn.close()


if __name__ == '__main__':
    createUserTable()
    InsertStartingData()
    print(User.getAllUsers())
import sqlite3

class Tool:
    def __init__(self, id, userID, title, desc, imgPath, category, availability, datePosted):
        self.__id = id
        self.__userID = userID
        self.__title = title
        self.__description = desc
        self.__imgPath = imgPath
        self.__category = category
        self.__availability = availability
        self.__datePosted = datePosted

   
    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value):
        self.__title = value

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value):
        self.__description = value

    @property
    def category(self):
        return self.__category

    @category.setter
    def category(self, value):
        self.__category = value
    
    @property
    def imgPath(self):
        return self.__imgPath

    @imgPath.setter
    def imgPath(self, value):
        self.__imgPath = value

    @property
    def availability(self):
        return self.__availability

    @availability.setter
    def availability(self, value):
        self.__availability = value

    def __str__(self):
        return "Resource Title: {} \n Description: {} \n Category: {} \n Availability: {} \n Date Posted: {}".format(self.title, self.description,self.category,self.availability,self.datePosted)
    
    @classmethod
    def delTool(cls, id):
        conn = None
        conn = sqlite3.connect( "database.db")
        sql='DELETE FROM tools WHERE id=?'
        cur = conn.cursor()
        cur.execute(sql, (id,))
        conn.commit()
        conn.close()

    @classmethod
    def addTool(cls, id, userID, title, desc, imgPath, category, availability, datePosted):
        conn = None
        conn = sqlite3.connect( "database.db")
        sql='INSERT INTO tools (id, user_id, title, description, imgPath, category, availability, datePosted) values (?,?,?,?,?,?,?,?)'
        cur = conn.cursor()
        cur.execute(sql, (id, userID, title, desc, imgPath, category, availability, datePosted, ))
        conn.commit()
        if conn:
            conn.close()

    @classmethod
    def addToolNoPic(cls, id, userID, title, desc, category, availability, datePosted):
        conn = None
        conn = sqlite3.connect( "database.db")
        sql='INSERT INTO tools (id, user_id, title, description, category, availability, datePosted) values (?,?,?,?,?,?,?)'
        cur = conn.cursor()
        cur.execute(sql, (id, userID, title, desc, category, availability, datePosted, ))
        conn.commit()
        if conn:
            conn.close()

    @classmethod
    def updateTool(cls, id, title, desc, imgPath, category, availability, datePosted):
        conn = None
        conn = sqlite3.connect('database.db')
        sql='UPDATE tools SET title=?, description=?, imgPath=?, category=?, availability=?, datePosted = ? WHERE id = ?'
        cur = conn.cursor()
        cur.execute(sql, (title, desc, imgPath, category, availability, datePosted,id,))
        conn.commit()
        conn.close()

    @classmethod
    def updateToolNoPic(cls, id, title, desc, category, availability, datePosted):
        conn = None
        conn = sqlite3.connect('database.db')
        sql='UPDATE tools SET title=?, description=?, category=?, availability=?, datePosted = ? WHERE id = ?'
        cur = conn.cursor()
        cur.execute(sql, (title, desc, category, availability, datePosted,id,))
        conn.commit()
        conn.close()

    @classmethod
    def getAllTools(cls):
        conn = sqlite3.connect('database.db')
        cursorObj = conn.cursor()
        cursorObj.execute('SELECT id, user_id, title, description, imgPath, category, availability, datePosted FROM tools;')
        allRows = cursorObj.fetchall()
        ListOfDictionaries = []
        for row in allRows:
            m = {"id" : row[0], "user_id": row[1], "title":row[2], 'description': row[3], 'imgPath':row[4], 'category':row[5], 'availability':row[6], 'datePosted':row[7] }
            ListOfDictionaries.append(m)
        if conn:
            conn.close()
        return ListOfDictionaries
    
    @classmethod
    def getTool(cls,tool_id):
        conn = sqlite3.connect('database.db')
        cursorObj = conn.cursor()
        cursorObj.execute('SELECT id, user_id, title, description, imgPath, category, availability, datePosted FROM tools WHERE id=?;',(tool_id,))
        allRows = cursorObj.fetchone()
        m = {"id" : allRows[0], "user_id": allRows[1], "title":allRows[2], 'description': allRows[3], 'imgPath':allRows[4], 'category':allRows[5], 'availability':allRows[6], 'datePosted':allRows[7] }
        if conn:
            conn.close()
        return m
    
    @classmethod 
    def getToolsForUser(cls,user_id):
        conn = sqlite3.connect('database.db')
        cursorObj = conn.cursor()
        cursorObj.execute('SELECT id, user_id, title, description, imgPath, category, availability, datePosted FROM tools WHERE user_id=?;',(user_id,))
        allRows = cursorObj.fetchall()
        ListOfDictionaries = []
        for row in allRows:
            m = {"id" : row[0], "user_id": row[1], "title":row[2], 'description': row[3], 'imgPath':row[4], 'category':row[5], 'availability':row[6], 'datePosted':row[7] }
            ListOfDictionaries.append(m)
        if conn:
            conn.close()
        return ListOfDictionaries
    

def InsertStartingData():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    tool_data = [
        (1, 1, 'Vintage Radio', 'A well-preserved vintage radio from the 1970s', None, 'Electronics', 'available', '2023-01-11'),
        (2, 2, 'Gardening Tools', 'Set of basic gardening tools, barely used', None, 'Hardware', 'available', '2023-01-06')]
    cur.executemany('''INSERT INTO tools (id, user_id, title, description, imgPath, category, availability, datePosted) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', tool_data)
    conn.commit()
    conn.close()

def createToolTable():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE Tools (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, title TEXT NOT NULL, description TEXT, imgPath TEXT, category TEXT, availability TEXT, datePosted TEXT NOT NULL, FOREIGN KEY (user_id) REFERENCES Users(user_id));''')
    conn.commit()
    conn.close()


if __name__ == '__main__':
    createToolTable()
    InsertStartingData()
    print(Tool.getAllTools())
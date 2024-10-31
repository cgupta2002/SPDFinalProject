import sqlite3

class Review:
    def __init__(self, review_id, user_id, reviewer_id, rating, content, timestamp):
        self.__review_id = review_id
        self.__user_id = user_id
        self.__reviewer_id = reviewer_id
        self.__rating = rating
        self.__content = content
        self.__timestamp = timestamp

    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, value):
        self.__content = value

    @property
    def review_id(self):
        return self.__review_id
    
    @property
    def user_id(self):
        return self.__user_id
    
    @property
    def rating(self):
        return self.__rating
    
    @rating.setter
    def rating(self, value):
        self.__rating = value
    
    @property
    def timestamp(self):
        return self.__timestamp
    
    @property
    def reviewer_id(self):
        return self.__reviewer_id

    def __str__(self):
        return "User: {} \n Reviewer: {} \n Rating: {} \n Content: {} \n Timestamp: {}".format(self.user_id, self.reviewer_id,self.content,self.timestamp)
    
    @classmethod
    def delReview(cls, review_id):
        conn = None
        conn = sqlite3.connect( "database.db")
        sql='DELETE FROM reviews WHERE review_id=?'
        cur = conn.cursor()
        cur.execute(sql, (review_id,))
        conn.commit()
        conn.close()

    @classmethod
    def addReview(cls, review_id, user_id, reviewer_id, rating, content, timestamp):
        conn = None
        conn = sqlite3.connect( "database.db")
        sql='INSERT INTO reviews (review_id, user_id, reviewer_id, rating, content, timestamp) values (?,?,?,?,?,?)'
        cur = conn.cursor()
        cur.execute(sql, ( review_id, user_id, reviewer_id, rating, content, timestamp,))
        conn.commit()
        if conn:
            conn.close()

    @classmethod
    def editReview(cls, review_id, rating, content, timestamp):
        conn = None
        conn = sqlite3.connect('database.db')
        sql='UPDATE reviews SET rating=?, content=?, timestamp=? WHERE review_id = ?'
        cur = conn.cursor()
        cur.execute(sql, ( review_id, rating, content, timestamp,))
        conn.commit()
        conn.close()

    @classmethod
    def getAllReviews(self):
        conn = sqlite3.connect('database.db')
        cursorObj = conn.cursor()
        cursorObj.execute('SELECT review_id, user_id, reviewer_id, rating, content, timestamp FROM reviews;')
        allRows = cursorObj.fetchall()
        ListOfDictionaries = []
        for row in allRows:
            m = {"review_id": row[0], "user_id":row[1], 'reviewer_id': row[2], 'rating':row[3], 'content':row[4], 'timestamp':row[5]}
            ListOfDictionaries.append(m)
        if conn:
            conn.close()
        return ListOfDictionaries
    
    

def InsertStartingData():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    review_data = [
        (1, 1, 2, 5, 'Great exchange experience!', '2023-01-16'),
        (2, 2, 1, 4, 'Items were as described, smooth process.', '2023-01-17')]
    cur.executemany('''INSERT INTO reviews (review_id, user_id, reviewer_id, rating, content, timestamp) VALUES (?, ?, ?, ?, ?, ?)''', review_data)
    conn.commit()
    conn.close()

def createReviewTable():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE reviews (review_id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER,reviewer_id INTEGER,rating INTEGER NOT NULL,content TEXT,timestamp TEXT NOT NULL,FOREIGN KEY (user_id) REFERENCES users(user_id),FOREIGN KEY (reviewer_id) REFERENCES users(user_id));''')
    conn.commit()
    conn.close()


if __name__ == '__main__':
    createReviewTable()
    InsertStartingData()
    print(Review.getAllReviews())
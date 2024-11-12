CREATE TABLE IF NOT EXISTS Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    profile_image TEXT,
    location TEXT
);

INSERT INTO Users (user_id, username, name, email, password, profile_image, location) VALUES
(1, 'jdoe123', 'John Doe', 'johndoe@example.com', 'hashed_password_1', NULL, 'New York, NY'),
(2, 'jsmith2030', 'Jane Smith', 'janesmith@example.com', 'hashed_password_2', NULL, 'Los Angeles, CA');

CREATE TABLE IF NOT EXISTS Tools (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    title TEXT NOT NULL,
    description TEXT,
    imgPath TEXT,
    category TEXT,
    availability TEXT,
    datePosted TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

INSERT INTO Tools (id, user_id, title, description, imgPath, category, availability, datePosted) VALUES
(1, 1, 'Vintage Radio', 'A well-preserved vintage radio from the 1970s', NULL, 'Electronics', 'available', '2023-01-11'),
(2, 2, 'Gardening Tools', 'Set of basic gardening tools, barely used', NULL, 'Hardware', 'available', '2023-01-06');

CREATE TABLE IF NOT EXISTS Reviews (
    user_id INTEGER,
    reviewer_id INTEGER,
    rating INTEGER NOT NULL,
    content TEXT,
    timestamp TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (reviewer_id) REFERENCES Users(user_id)
);

INSERT INTO Reviews (user_id, reviewer_id, rating, content, timestamp) VALUES
(1, 2, 5, 'Great exchange experience!', '2023-01-16'),
(2, 1, 4, 'Items were as described, smooth process.', '2023-01-17');

CREATE TABLE IF NOT EXISTS Conversations (
    conversation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    participant1_id INTEGER NOT NULL,
    participant2_id INTEGER NOT NULL,
    message_ids TEXT,
    FOREIGN KEY (participant1_id) REFERENCES Users(user_id),
    FOREIGN KEY (participant2_id) REFERENCES Users(user_id)
);

CREATE TABLE IF NOT EXISTS Messages (
    message_id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id INTEGER NOT NULL,
    sender_id INTEGER NOT NULL,
    receiver_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    FOREIGN KEY (conversation_id) REFERENCES Conversations(conversation_id),
    FOREIGN KEY (sender_id) REFERENCES Users(user_id),
    FOREIGN KEY (receiver_id) REFERENCES Users(user_id)
);

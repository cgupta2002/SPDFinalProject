CREATE TABLE Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    profile_image TEXT,
    location TEXT
);

INSERT INTO Users (user_id, name, email, password, profile_image, location) VALUES
(1, 'John Doe', 'johndoe@example.com', 'hashed_password_1', '/images/johndoe.jpg', 'New York, NY'),
(2, 'Jane Smith', 'janesmith@example.com', 'hashed_password_2', '/images/janesmith.jpg', 'Los Angeles, CA');

CREATE TABLE Tools (
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
(1, 1, 'Vintage Radio', 'A well-preserved vintage radio from the 1970s', '/images/listing1.jpg', 'Electronics', 'available', '2023-01-11'),
(2, 2, 'Gardening Tools', 'Set of basic gardening tools, barely used', '/images/listing2.jpg', 'Gardening', 'available', '2023-01-06');

CREATE TABLE Messages (
    message_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER,
    receiver_id INTEGER,
    content TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    FOREIGN KEY (sender_id) REFERENCES Users(user_id),
    FOREIGN KEY (receiver_id) REFERENCES Users(user_id)
);

INSERT INTO Messages (message_id, sender_id, receiver_id, content, timestamp) VALUES
(1, 2, 1, 'Is the radio still available?', '2023-01-13 10:15 AM'),
(2, 1, 2, 'I''m interested in the gardening tools!', '2023-01-14 02:20 PM');

CREATE TABLE Reviews (
    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    reviewer_id INTEGER,
    rating INTEGER NOT NULL,
    comment TEXT,
    timestamp TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (reviewer_id) REFERENCES Users(id)
);

INSERT INTO Reviews (review_id, user_id, reviewer_id, rating, comment, timestamp) VALUES
(1, 1, 2, 5, 'Great exchange experience!', '2023-01-16'),
(2, 2, 1, 4, 'Items were as described, smooth process.', '2023-01-17');

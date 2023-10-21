
CREATE DATABASE wishes;

USE wishes;

CREATE TABLE register_a_wisher(
    user_id INT,
    first_name VARCHAR(30),
    last_name VARCHAR(30),
    email VARCHAR(65),
    phone_number VARCHAR(15)
);

CREATE TABLE make_a_wish(
    full_name VARCHAR(100),
    describe_your_wish TEXT,
    when_you_want_it_to_happen TEXT
);

SELECT * FROM register_a_wisher;
SELECT * FROM make_a_wish; 

DROP TABLE register_a_wisher;
DROP TABLE make_a_wish;

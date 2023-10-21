# The MIT License (MIT)
# Copyright © 2023 GitPhantom

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the “Software”), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
# Step 1: Import necessary libraries and modules
import string
import secrets
import bcrypt
import sqlite3
import random

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('database.db')

# Create a cursor
cursor = conn.cursor()

# Create a table
cursor.execute('CREATE TABLE IF NOT EXISTS hash_tb (id INTEGER PRIMARY KEY, origin_str TEXT, hashed_str TEXT, hash_count INTEGER)')

# This function is responsible for generating the str randomly.
def generate_random_str(hash_count, str_length):
    alphabet = string.ascii_letters + string.digits  # You can customize this as needed
    random_str = ''.join(secrets.choice(alphabet) for _ in range(str_length))

    hashed_str = random_str.encode('utf-8')
    for index in range(hash_count):
        hashed_str = bcrypt.hashpw(hashed_str, bcrypt.gensalt())

    insert_str_to_db(random_str, hashed_str, hash_count)
    return {origin_str: random_str, hashed_str}


# This function is responsible for generating the str.
def select_str_list(str_count, complexity):
    cursor.execute("SELECT * FROM hash_tb where hash_count = ? limit ?", (complexity, str_count))
    rows = cursor.fetchall()
    missing_count = max(str_count - len(rows), 0)

    origin_str_list = []
    hashed_str_list = []

    new_count = 0

    if random.random() >= 0.7:
        new_count += random.randint(0, 3)

    for index in range(missing_count + new_count):
        pair_str = generate_random_str(complexity, 10)
        origin_str_list.append(pair_str['origin_str'])
        hashed_str_list.append(pair_str['hashed_str'])
    
    for row_i in rows:
        if len(origin_str_list) > str_count:
            break
        origin_str_list.append(row_i['origin_str'])
        hashed_str_list.append(row_i['hashed_str'])

    return {'origin' : origin_str_list, 'hashed' : hashed_str_list}

# This function is responsible for inserting the str to db.
def insert_str_to_db(origin_str, hashed_str, hash_count):
    # Insert data
    cursor.execute("INSERT INTO hash_tb (origin_str, hashed_str, hash_count) VALUES (?, ?)", (origin_str, hashed_str, hash_count))


# This function is responsible for evaluating the hashed_str with the database
def evaluate(answer_str_list, result_str_list):
    right_count = 0.0
    count = len(answer_str_list)
    for i, answer_i in answer_str_list:
        if answer_i == result_str_list[i]:
            right_count += 1
    return right_count / count

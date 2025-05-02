d = {
  "users": [
    {
      "id": 1,
      "username": "user123",
      "email": "user123@example.com",
      "phone": "+1234567890",
      "password": "hashed_password_here",
      "salt": "random_salt_for_hashing"
    },
    {
      "id": 2,
      "username": "john_doe",
      "email": "john.doe@example.com",
      "phone": "+9876543210",
      "password": "another_hashed_password",
      "salt": "another_random_salt"
    }
  ]
}

logins = {x["phone"] for x in d["users"]}
emails = {x["email"] for x in d["users"]}
nums = {x["username"] for x in d["users"]}
print(d)
print(logins)
print(emails)
print(nums)
from app import User
user=User.query.first()
print(user.username)
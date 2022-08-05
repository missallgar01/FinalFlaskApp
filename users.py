class Users():
    """Class for user login authentication"""
    def __init__(self):
        """Constructor Method"""
        self.file = open('data/users.csv', 'r')


    def authenticate(self, username, password):
        """Method to complete user login authentication"""
        all_lines = self.file.readlines()
        found = False
        for line in all_lines:
            if username in line and password in line:
                found = True
                break  # no need to check other lines
        self.file.close()
        return found

if __name__ == '__main__':
    user_login = Users()
    result = user_login.authenticate('test', 'test')
    print(result)

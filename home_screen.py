from database import *
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QDialog
from decimal import Decimal

class HomeScreen(QDialog):
    def __init__(self,username):
        mydb, cursor = initialize_connection()
        super(HomeScreen,self).__init__()
        loadUi("customer_actions.ui", self)
        name = return_information_using_username(cursor,"name",username,)
        self.username = username
        self.welcome_label.setText(f"Welcome {name}")
        self.update_button.clicked.connect(self.go_to_update_details)
        self.history_button.clicked.connect(self.go_to_transaction_history)
        self.balance_button.clicked.connect(self.go_to_balance)
        self.deposit_button.clicked.connect(self.go_to_deposit)
        self.withdraw_button.clicked.connect(self.go_to_withdraw)
        self.transfer_button.clicked.connect(self.go_to_transfer)
        self.logout_button.clicked.connect(self.logout)

    def go_to_update_details(self):
        self.ui = UpdateDetailsWindow(self.username)
        self.ui.setMinimumSize(450,350)
        self.ui.show()
        self.close()

    def go_to_transaction_history(self):
        self.ui = TransactionHistoryWindow(self.username)
        self.ui.setMinimumSize(450,350)
        self.ui.show()
        self.close()

    def go_to_balance(self):
        self.ui = BalanceWindow(self.username)
        self.ui.setMinimumSize(450,350)
        self.ui.show()
        self.close()

    def go_to_deposit(self):
        self.ui = DepositWindow(self.username)
        self.ui.setMinimumSize(450,350)
        self.ui.show()
        self.close()

    def go_to_withdraw(self):
        self.ui = WithdrawWindow(self.username)
        self.ui.setMinimumSize(450, 350)
        self.ui.show()
        self.close()

    def go_to_transfer(self):
        self.ui = TransferWindow(self.username)
        self.ui.setMinimumSize(450, 350)
        self.ui.show()
        self.close()

    def logout(self):
        self.close()


class TransactionHistoryWindow(QDialog):
    def __init__(self,username):
        mydb, cursor = initialize_connection()
        super(TransactionHistoryWindow,self).__init__()
        loadUi("transaction_history.ui", self)
        self.username = username
        name = return_information_using_username(cursor,"name",username,)
        self.welcome_label_2.setText(f"Welcome {name}")
        self.home_button.clicked.connect(self.home_screen)
        self.transaction_history = "Account# | Action | Amount | Date \n"

        cursor.execute(f"SELECT * FROM {self.username}_transactions")
        self.fetch_all = cursor.fetchall()
        for i in self.fetch_all:
            self.transaction_history += f"\n{i[0]}    {i[1]}     {i[2]}      {i[3]}"

        self.transaction_history_label.setText(self.transaction_history)

    def home_screen(self):
        self.ui = HomeScreen(self.username)
        self.ui.setMinimumSize(450,350)
        self.ui.show()
        self.close()

class UpdateDetailsWindow(QDialog):
    def __init__(self,username):
        super(UpdateDetailsWindow,self).__init__()
        loadUi("update_details.ui", self)
        self.username = username
        self.username = username
        self.update_button.clicked.connect(self.update_details)
        self.home_button.clicked.connect(self.go_to_home_screen)

    def update_details(self):
        mydb, cursor = initialize_connection()
        updated_name = self.name_input.text()
        updated_username = self.username_input.text()
        updated_password = self.password_input.text()
        user_data = {"name": updated_name, "username": updated_username, "password": updated_password}

        for char in updated_name:
            if not char.isalpha() and not char.isspace():
                 self.error_text.setText("Error: Name must have only letters or spaces")
                 return
        if len(updated_name)==0 or len(updated_username)==0 or len(updated_password)==0:
            self.error_text.setText("Error: No field can be left empty")
            return
        elif username_not_available(cursor, user_data):
            self.error_text.setText("Error: Username already exists")
            return
        elif len(updated_name)>70:
            self.error_text.setText("Error: Name cannot be more than 70 characters long")
            return
        elif len(updated_username) > 50 or len(updated_username) < 8:
            self.error_text.setText("Error: Username must be from 8-50 characters long")
            return
        elif len(updated_password) < 12 or len(updated_password) > 50:
            self.error_text.setText("Error: Password must be from 12-50 characters long")
            return
        else:
            self.error_text.setText("")
            cursor.execute(f"UPDATE user_info SET name= '{updated_name}', username='{updated_username}', password='{updated_password}' WHERE username='{self.username}'")
            mydb.commit()
            cursor.execute(f"ALTER TABLE {self.username}_transactions RENAME TO {updated_username}_transactions")
            mydb.commit()
            self.username = updated_username

    def go_to_home_screen(self):
        self.ui = HomeScreen(self.username)
        self.ui.setMinimumSize(450,350)
        self.ui.show()
        self.close()

class BalanceWindow(QDialog):
    def __init__(self,username):
        mydb, cursor = initialize_connection()
        super(BalanceWindow,self).__init__()
        loadUi("balance.ui", self)
        self.username = username
        self.balance = return_information_using_username(cursor,"balance",username)
        name = return_information_using_username(cursor,"name",username)
        self.user_balance_label.setText('$'+ str(self.balance) )
        self.welcome_label_2.setText(f"Welcome {name}")
        self.home_button.clicked.connect(self.home_screen)

    def home_screen(self):
        self.ui = HomeScreen(self.username)
        self.ui.setMinimumSize(450,350)
        self.ui.show()
        self.close()

class DepositWindow(QDialog):
    def __init__(self,username):
        super(DepositWindow,self).__init__()
        loadUi('deposit.ui',self)
        mydb, cursor = initialize_connection()
        self.balance = return_information_using_username(cursor,"balance",username)
        name = return_information_using_username(cursor,"name",username)
        self.username = username
        self.user_balance_label.setText('$'+ str(self.balance) )
        self.welcome_label_2.setText(f"Welcome {name}")
        self.deposit_button.clicked.connect(self.deposit_function)
        self.home_button.clicked.connect(self.home_screen)

    def deposit_function(self):
        deposit_amount = self.deposit_input.text()

        if not deposit_amount.isalpha():
            mydb, cursor = initialize_connection()
            try:
                decimal_deposit = Decimal(deposit_amount)
            except:
                self.response_message.setText("Error: Must enter a valid input")
                return

            self.response_message.setText("")
            new_balance = self.balance + decimal_deposit
            cursor.execute(f"UPDATE user_info SET balance = {new_balance} WHERE username = '{self.username}'")
            mydb.commit()

            account_num = return_information_using_username(cursor,"account_number",self.username)
            insert_into_transaction_table(cursor,mydb,self.username,account_num,"Deposit",decimal_deposit)

            self.balance = return_information_using_username(cursor, "balance", self.username)
            self.user_balance_label.setText('$' + str(self.balance))

        else:
            self.response_message.setText("Error: Must enter a valid input")
            return

    def home_screen(self):
        self.deposit_input.clear()

        self.ui = HomeScreen(self.username)
        self.ui.setMinimumSize(450,350)
        self.ui.show()
        self.close()

class WithdrawWindow(QDialog):
    def __init__(self,username):
        super(WithdrawWindow,self).__init__()
        loadUi('withdraw.ui', self)
        mydb, cursor = initialize_connection()
        name = return_information_using_username(cursor,"name",username)
        self.balance = return_information_using_username(cursor,"balance",username)
        self.username = username
        self.user_balance_label.setText('$'+ str(self.balance) )
        self.welcome_label_2.setText(f"Welcome {name}")
        self.withdraw_button_2.clicked.connect(self.withdraw_function)
        self.home_button.clicked.connect(self.home_screen)

    def withdraw_function(self):
        mydb, cursor = initialize_connection()
        withdraw_amount = self.withdraw_input.text()
        if not withdraw_amount.isalpha():
            try:
                decimal_withdraw = Decimal(withdraw_amount)
            except:
                self.response_message.setText("Error: Must enter a valid input")
                return

            if self.balance>decimal_withdraw:
                self.response_message.setText("")
                new_balance = self.balance - decimal_withdraw
                cursor.execute(f"UPDATE user_info SET balance = {new_balance} WHERE username = '{self.username}'")
                mydb.commit()

                account_num = return_information_using_username(cursor, "account_number", self.username)
                insert_into_transaction_table(cursor, mydb, self.username, account_num, "Withdrawal", decimal_withdraw)

                self.balance = return_information_using_username(cursor, "balance", self.username)
                self.user_balance_label.setText('$' + str(self.balance))
            else:
                 self.response_message.setText("Error: Cannot withdraw amount more than balance")
                 return

        else:
            self.response_message.setText("Error: Must enter a valid input")
            return

    def home_screen(self):
        self.withdraw_input.clear()

        self.ui = HomeScreen(self.username)
        self.ui.setMinimumSize(450,350)
        self.ui.show()
        self.close()

class TransferWindow(QDialog):
    def __init__(self,username):
        mydb, cursor = initialize_connection()
        super(TransferWindow,self).__init__()
        loadUi("transfer.ui", self)
        name = return_information_using_username(cursor,"name",username)
        self.balance = return_information_using_username(cursor,"balance",username)
        self.username = username
        self.user_balance_label.setText('$'+ str(self.balance) )
        self.welcome_label_2.setText(f"Welcome {name}")
        self.transfer_button.clicked.connect(self.transfer_function)
        self.home_button_3.clicked.connect(self.home_screen)

    def transfer_function(self):
        mydb, cursor = initialize_connection()
        transfer_amount = self.transfer_input.text()
        account_number = self.account_number_input.text()

        if not transfer_amount.isalpha() and not account_number.isalpha():
            try:
                decimal_transfer = Decimal(transfer_amount)
            except:
                self.response_message.setText("Error: Must enter a valid input")
                return

            if self.balance < decimal_transfer:
                self.response_message.setText("Error: Cannot transfer amount more than balance")
                return
            elif not account_number_available(cursor,account_number):
                self.response_message.setText("Error: Account number does not exist")
                return
            else:
                self.response_message.setText("")
                sender_balance = self.balance - decimal_transfer
                receiver_balance = return_information_using_account_number(cursor, "balance", account_number) + decimal_transfer

                cursor.execute(f"UPDATE user_info SET balance = {sender_balance} WHERE username = '{self.username}'")
                mydb.commit()
                transferred_account_num = return_information_using_username(cursor, "account_number", self.username)
                insert_into_transaction_table(cursor, mydb, self.username, transferred_account_num, "Transferred", decimal_transfer)

                cursor.execute(f"UPDATE user_info SET balance = {receiver_balance} WHERE account_number = '{account_number}'")
                mydb.commit()
                username = return_information_using_account_number(cursor, "username", account_number)
                insert_into_transaction_table(cursor, mydb, username, account_number, "Received", transfer_amount)


                self.balance = return_information_using_username(cursor, "balance", self.username)
                self.user_balance_label.setText('$' + str(self.balance))

        else:
            self.response_message.setText("Error: Must enter a valid input")
            return

    def home_screen(self):
        self.transfer_input.clear()

        self.ui = HomeScreen(self.username)
        self.ui.setMinimumSize(450,350)
        self.ui.show()
        self.close()




# # import pytest
# # from app.calculation import add

# # @pytest.mark.parametrize('num_1, num_2, expected', [(4,3,7)])

# # def test_add(num_1, num_2, expected):
# #     print('Testing the function')
# #     #sum = add(5, 3)
# #     assert add(num_1, num_2) == expected

# import pytest
# from app.calculation import add, subtract, multiply, divide, BankAccount

# @pytest.fixture
# def zero_bank_account():
#     print('creating a bank account')
#     return BankAccount(0)

# @pytest.fixture
# def bank_account():
#     return BankAccount(50)


# # Parameterized test case
# @pytest.mark.parametrize('num_1, num_2, expected', [
#     (4, 3, 7)  # Test with numbers 4 and 3, expecting the sum to be 7
# ])
# def test_add(num_1, num_2, expected):
#     print('Testing the function')
#     assert add(num_1, num_2) == expected


# def test_subtraction():
#     assert subtract(9,4) == 5


# def test_multiply():
#     assert multiply(9,4) == 36


# def test_divide():
#     assert divide(9,4) == 2.25



# def test_bank_set_initial_amount():
#     bank_account = BankAccount(50)
#     assert bank_account.balance == 50


# def test_bank_default_amount():
#     bank_account = BankAccount()
#     print('Testing my bank account')
#     assert bank_account.balance == 0


# # def test_deposite():
# #     bank_account = BankAccount(0)
# #     account_depo = bank_account.deposite(900)
# #     assert bank_account.balance ==  account_depo
# #     assert bank_account.balance == 900
    
# def test_deposite():
#     bank_account = BankAccount(0)
#     account_depo = bank_account.deposite(900)
#     assert bank_account.balance == account_depo
#     assert bank_account.balance == 900


# def test_withdraw(bank_account):
#     bank_account = BankAccount(900)
#     bank_account.withdraw(330)
#     #assert bank_account.balance == bank_account
#     assert bank_account.balance == 570


# def test_collect(bank_account):
#    # bank_account = BankAccount(50)
#     bank_account.interest((1.1))
#     assert round(bank_account.balance, 2) == 55


# def test_bank_tranction(zero_bank_account):
#     zero_bank_account.deposite(200)
#     zero_bank_account.withdraw(100)
#     assert zero_bank_account.balance == 100


# def test_insuffient_funds(bank_account):
#     with pytest.raises(Exception):
#         bank_account.withdraw(200)









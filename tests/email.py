# import pytest
# from mailer import construct_email_message, construct_email_template, get_emails, send_message


# def test_get_emails():
#     email_list = get_emails('tests/test_emails.csv')
#     # assert len(email_list) > 0
#     # assert '@' in email_list[0]
#     print(email_list)


# def test_get_emails_fail():
#     with pytest.raises(FileNotFoundError):
#         get_emails('tests/test_emails2.csv')


# def main():
#     test_get_emails()
#     # test_get_emails_fail()

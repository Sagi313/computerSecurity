def is_input_text_valid(text, max_length, min_length):
    len_text = len(text)
    if len_text > max_length or len_text < min_length:
        return False
    return True

def is_valid_name(name):
    return name.isalpha()
    
def is_valid_email(email):
    if not (email.find('@') and email.find('.')):
        return email.find('@') < email.find('.')
    return False
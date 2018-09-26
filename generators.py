import random
import string


def _generate_string_from_chars(char_list, length):
    random_chars = random.choices(char_list, k=length)
    return ''.join(random_chars)


def generate_alpha_string(length):
    return _generate_string_from_chars(string.ascii_letters, length)


def generate_alphanum_string(length):
    char_list = string.ascii_letters + string.digits
    return _generate_string_from_chars(char_list, length)


def generate_num_string(length):
    return _generate_string_from_chars(string.digits, length)


def generate_integer(start, stop):
    return random.randint(start, stop)


if __name__ == '__main__':
    length = 60
    print(generate_alpha_string(length))
    print(generate_num_string(length))
    print(generate_alphanum_string(length))
    print(generate_integer(0, length))

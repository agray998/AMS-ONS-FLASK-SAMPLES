from app import random_func_name, random_func_2

def test_random_func():
    assert random_func_name() == "Hello World!sample text"
    assert random_func_2() == "sample text"
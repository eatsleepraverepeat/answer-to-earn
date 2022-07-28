import pytest


def test_ownership(get_question_token):
    NULL_ADDR = "0x0000000000000000000000000000000000000000"
    assert get_question_token.owner() == NULL_ADDR

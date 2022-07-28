import pytest
from web3 import Web3
from brownie import Question, QuestionToken, QuestionFactory
from utils.units import toWei, fromWei


@pytest.fixture(scope="function", autouse=True)
def isolation(fn_isolation):
    pass

@pytest.fixture(scope='module')
def get_question_token(get_accounts):
    _, _, _sys = get_accounts
    return QuestionToken.deploy({"from": _sys})

@pytest.fixture(scope='module')
def get_accounts(accounts):
    # questioner, expert, _sys
    yield accounts[1], accounts[-1], accounts[0]

@pytest.fixture(scope='function')
def get_question_abi():
    yield Question.abi

@pytest.fixture(scope='module')
def get_question_factory(get_accounts):
    _, _, _sys = get_accounts
    yield QuestionFactory.deploy({"from": _sys})

@pytest.fixture(scope='function', autouse=True)
def mint_tokens(get_question_token, get_accounts):
    questioner, expert, _sys = get_accounts
    get_question_token.mint(questioner, int(get_question_token.s_maxSupply() * 0.5), {"from": _sys})
    get_question_token.renounceOwnership({"from": _sys})

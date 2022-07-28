import pytest
import brownie
from brownie import Question
from web3 import Web3
from utils.units import toWei, fromWei


@pytest.mark.parametrize(
    'question, reward, answer', [
        ('What is the meaning of life?', 10, '42'),
        ('My Macbook Air weights 2.3 pounds. If I download more files on it, will it make it heavier?', 5, 'No'),
        ('If I hire a hitman to kill me and he fails, will I go to jail?', 666, 'Snake bites itself'),
        ('Is blockchain development worth to master?', 100, 'Most likely, yes')
    ]
)
def test_question_success(
    question, reward, answer, 
    get_question_token, get_accounts):
    
    questioner, expert, _ = get_accounts
    
    # question contract part
    _question = Question.deploy(question, questioner, get_question_token.address, toWei(reward), {"from": questioner})
    assert _question.question() == question
    assert _question.active()
    assert _question.tx.events['QuestionStatus']['active']

    # question funding, fails
    with brownie.reverts('ERC20: transfer amount exceeds allowance'):
        _question.fund({"from": questioner})

    # approval and allowance
    assert not get_question_token.allowance(questioner, _question, {"from": questioner})
    get_question_token.approve(_question.address, toWei(reward), {"from": questioner})
    assert get_question_token.allowance(questioner, _question, {"from": questioner}) == toWei(reward)

    # question funding, success
    _question.fund({"from": questioner})
    assert get_question_token.balanceOf(_question.address) == toWei(reward)

    # the only given answer is accepted, for the sake of simplicity
    tx = _question.accept_answer(expert, answer, {"from": questioner})
    assert tx.events.keys() == ['Transfer', 'QuestionStatus', 'AnswerAccepted']
    assert tx.events['Transfer']['value'] == toWei(reward)
    assert not tx.events['QuestionStatus']['active']
    assert tx.events['AnswerAccepted']['answer'] == answer
    
    assert not _question.active()
    assert _question.accepted() == answer
    assert get_question_token.balanceOf(expert) == toWei(reward)


@pytest.mark.parametrize(
    'question, reward, answer', [
        ('What is the meaning of life?', 10, '42'),
        ('My Macbook Air weights 2.3 pounds. If I download more files on it, will it make it heavier?', 5, 'No'),
        ('If I hire a hitman to kill me and he fails, will I go to jail?', 666, 'Snake bites itself'),
        ('Is blockchain development worth to master?', 100, 'Most likely, yes')
    ]
)
def test_question_failed(
    question, reward, answer, 
    get_question_token, get_accounts):
    
    questioner, expert, _ = get_accounts
    
    # question contract part
    _question = Question.deploy(question, questioner, get_question_token.address, toWei(reward), {"from": questioner})
    
    # approval (expert)
    get_question_token.approve(_question.address, toWei(reward), {"from": expert})

    with brownie.reverts('QuestionContract: why da heck you need to fund someone question?'):
        _question.fund({"from": expert})

    with brownie.reverts('QuestionContract: only questioner can accept answer'):
        _question.accept_answer(expert, answer, {"from": expert})

    assert _question.active()
    assert not _question.accepted()

    # approval (questioner)
    get_question_token.approve(_question.address, toWei(reward), {"from": questioner})

    _question.fund({"from": questioner})

    with brownie.reverts('QuestionContract: you play unfair, mate'):
            _question.accept_answer(questioner, answer, {"from": questioner})

    _question.accept_answer(expert, answer, {"from": questioner})
    
    with brownie.reverts('QuestionContract: question is closed, answer is accepted'):
        _question.accept_answer(expert, answer, {"from": questioner})

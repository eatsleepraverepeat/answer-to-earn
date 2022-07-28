import re
import pytest
from brownie import Contract
from utils.units import toWei, fromWei


@pytest.mark.parametrize(
    'questions, answers, rewards', [
        (
            ['What is the meaning of life?', 'If I hire a hitman to kill me and he fails, will I go to jail?', 'Is blockchain development worth to master?'],
            ['42', 'Snake bites itself', 'Most likely, yes'],
            [10, 20, 100]
        ), 
        (
            ['What is the meaning of life?', 'If I hire a hitman to kill me and he fails, will I go to jail?', 'Is blockchain development worth to master?'],
            ['42', 'Snake bites itself', 'Most likely, yes'],
            [100, 200, 500]
        ),
        (
            ['What is the meaning of life?', 'If I hire a hitman to kill me and he fails, will I go to jail?', 'Is blockchain development worth to master?'],
            ['42', 'Snake bites itself', 'Most likely, yes'],
            [1000, 50, 256]
        )
    ]
)
def test_factory(
    questions, answers, rewards, 
    get_question_factory, get_question_token, get_question_abi, get_accounts
):
    
    questioner, _, _ = get_accounts
    
    for question, _, reward in zip(questions, answers, rewards):
        tx = get_question_factory.placeQuestion(question, questioner, get_question_token.address, toWei(reward))
        assert 'QuestionPlaced' in tx.events.keys()

    assert len(get_question_factory.getQuestions()) == len(questions)
    for ix, _question in enumerate(get_question_factory.getQuestions()):
        question_contract = Contract.from_abi(address=_question, abi=get_question_abi, name='Question')
        assert question_contract.question() == questions[ix]
        assert question_contract.reward() == toWei(rewards[ix])
        assert question_contract.questioner() == questioner


@pytest.mark.parametrize(
    'questions, answers, rewards', [
        (
            ['What is the meaning of life?', 'If I hire a hitman to kill me and he fails, will I go to jail?', 'Is blockchain development worth to master?'],
            ['42', 'Snake bites itself', 'Most likely, yes'],
            [10, 20, 100]
        ), 
        (
            ['What is the meaning of life?', 'If I hire a hitman to kill me and he fails, will I go to jail?', 'Is blockchain development worth to master?'],
            ['42', 'Snake bites itself', 'Most likely, yes'],
            [100, 200, 500]
        ),
        (
            ['What is the meaning of life?', 'If I hire a hitman to kill me and he fails, will I go to jail?', 'Is blockchain development worth to master?'],
            ['42', 'Snake bites itself', 'Most likely, yes'],
            [1000, 50, 256]
        )
    ]
)
def test_pool(
    questions, answers, rewards, 
    get_question_factory, get_question_token, get_question_abi, get_accounts):
    
    questioner, _, _ = get_accounts

    for question, _, reward in zip(questions, answers, rewards):
        _ = get_question_factory.placeQuestion(question, questioner, get_question_token.address, reward)
    
    questions = get_question_factory.getQuestions()
    total = 0
    for _question in questions:
        quiz_game = Contract.from_abi(address=_question, abi=get_question_abi, name='Question')
        total += quiz_game.reward()
    
    assert total == sum(rewards)

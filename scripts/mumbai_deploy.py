from brownie import accounts, config, network
from web3 import Web3
from brownie import QuestionToken, QuestionFactory, Question, Contract


def main():
    
    _REWARD = 1

    assert network.is_connected()
    account = accounts.add(config['wallets']['from_key'])
    expert = accounts.add()
    assert account.balance() > 0

    if not len(QuestionToken):
        token = QuestionToken.deploy({"from": account})
    else:
        token = QuestionToken[-1]

    if token.balanceOf(account) <= Web3.toWei(_REWARD, 'ether'):
        _ = token.mint(account, Web3.toWei(_REWARD, 'ether'), {"from": account})

    if not len(QuestionFactory):
        factory = QuestionFactory.deploy({"from": account})
    else:
        factory = QuestionFactory[-1]

    # place some question, give answer and accept it
    Q = 'What is meaning of life and everything?'
    _ = factory.placeQuestion(Q, account, token.address, Web3.toWei(_REWARD, 'ether'), {"from": account})
    
    _question = Contract.from_abi('Question', factory.getQuestions()[-1], abi=Question.abi)
    
    _ = token.approve(_question, Web3.toWei(_REWARD, 'ether'), {"from": account})
    _ = _question.fund({"from": account})
    _ = _question.accept_answer(expert, '42', {"from": account})

    print(f"Question: [{_question.question()}], Answer: [{_question.accepted()}]")

if __name__ == '__main__':
    main()

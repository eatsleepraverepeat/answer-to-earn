from web3 import Web3


def toWei(amount: int) -> int:
    return Web3.toWei(amount, "ether")

def fromWei(amount: int) -> int:
    return Web3.fromWei(amount, "ether")

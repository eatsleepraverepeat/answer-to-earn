# Answer-To-Earn
## Toy backend of abstractive Answer-To-Earn dApp for placing, answering to and accepting of answers to a various questions

## Overview
I came across a simple idea to code an application, which gives opportunity to earn some money by sharing a knowledge. There are many related projects, such as Quora as an example, where experts sharing expertise in different domains in a form of answering questions. AFAIK non of them rewarding experts financialy and this simple project implements an answer-to-earn mechanic to battle this unfairity. Project were written for educational purposes and can only be treated in the same way.

## Specifics
This is a modified version of an idea, described in [**How To Build a Blockchain Gaming DApp | (Chainlink Engineering Tutorials**](https://www.youtube.com/watch?v=niqxn57vx9k) with the following changes:
- Supplement procedures (testing, deployment, etc) moved from [**`foundry`**](https://github.com/foundry-rs/foundry) to [**`brownie`**](https://github.com/eth-brownie/brownie), for all the Python folks out there;
- General mechanic is extended, such that funding and rewarding made in custom [**ERC20**](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/ERC20.sol) token called `QuestionToken`, where the one who placed a question can approve or accept someone answer for funds to be sent. Question itself, funding and accepting action has designed in respective smart-contract. Proceeding answers stored off-chain in mind (out of scope of this project), to not wasting gas as it many answers could be given. After completion accepted answer stored on-chain and question marked as inactive;
- Testing is also extended to cover all the logic with different cases

## Build and testing
```bash
conda env create -f environment.yml
conda activate eth-brownie
pipx install eth-brownie
brownie test . --network development  # tests will pass
```

More realistic testing should be done on target network, so we can use Polygon mainnet fork ([Alchemy](https://www.alchemy.com) API key required) by,
```bash
brownie networks add development polygon-main-fork-dev cmd=ganache-cli host=http://127.0.0.1 chain_id=137 fork='https://polygon-mainnet.g.alchemy.com/v2/<your-alchemy-api-key>' accounts=10 mnemonic=brownie port=8545
brownie test . --network polygon-main-fork-dev  # tests will pass
```

## Deploying on-chain, testnet
I'm using Polygon (Mumbai) for playing on live network, and [Alchemy](https://www.alchemy.com) as a node provider here. Before running the script make sure you have some [**MATIC**](https://coinmarketcap.com/ru/currencies/polygon/), to get them you cant this faucet [faucet](https://mumbaifaucet.com/).

```bash
export PRIVATE_KEY=<your-wallet-private-key>
brownie networks add Polygon alchemy_mumbai host='<your-app-view-key-https>' name='Mumbai (Alchemy)' chainid=80001 explorer='<mumbai-explorer-address>'
brownie run scripts/mumbai_deploy.py --networks alchemy_mumbai
```

## And, frontend?
Focusing on smart-contract development here, feel free to fork and [design one](https://youtu.be/niqxn57vx9k?t=3393).

## TODO
- Rewrite this project as a Program for Solana

// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import "contracts/Question.sol";

contract QuestionFactory {

    Question[] public questions;
    event QuestionPlaced(Question indexed question);

    constructor() {}

    function placeQuestion(string memory _question, address _questioner, address token_address, uint256 reward) public {
        Question question = new Question(_question, _questioner, token_address, reward);
        questions.push(question);
        emit QuestionPlaced(question);
    }

    function getQuestions() public view returns (Question[] memory) {
        return questions;
    }

}
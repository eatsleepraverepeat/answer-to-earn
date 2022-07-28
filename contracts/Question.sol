// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;


import "interfaces/QuestionTokenInterface.sol";

contract Question {

    address public questioner;
    string public question;
    string public accepted;
    address public token_address;
    uint256 public reward;
    bool public active;

    event QuestionStatus(bool active);
    event AnswerAccepted(string answer);

    constructor(string memory _question, address _questioner, address _token_address, uint256 _reward) {
        questioner = _questioner;
        question = _question;
        token_address = _token_address;
        reward = _reward;
        active = true;
        accepted = "";
        emit QuestionStatus(active);
    }

    function fund() public {
        require(msg.sender == questioner, 'QuestionContract: why da heck you need to fund someone question?');
        IQuestionTokenInterface(token_address).transferFrom(msg.sender, address(this), reward);
    }

    function accept_answer(address expert, string calldata answer) public {
        require(active == true, 'QuestionContract: question is closed, answer is accepted');
        require(questioner == msg.sender, 'QuestionContract: only questioner can accept answer');
        require(questioner != expert, 'QuestionContract: you play unfair, mate');
        complete(expert, answer);
        emit AnswerAccepted(answer);
    }

    function complete(address expert, string calldata answer) private {
        IQuestionTokenInterface(token_address).transfer(expert, reward);
        active = false;
        accepted = answer;
        emit QuestionStatus(active);
    }

    receive() external payable {}

}
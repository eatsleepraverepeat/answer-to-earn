// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract QuestionToken is ERC20, Ownable {
    uint256 public s_maxSupply = 10000000000000000000000;

    constructor() ERC20("QuestionToken", "QT") {}

    modifier supplyNotExceeded(uint256 amount) {
        require(totalSupply() + amount <= s_maxSupply, 'Supply limit exceeded!');
        _;
    }

    function mint(address account, uint256 amount) public onlyOwner() supplyNotExceeded(amount) {
        _mint(account, amount);
    }

    function burn(address account, uint256 amount) public onlyOwner() {
        _burn(account, amount);
    }
    
}

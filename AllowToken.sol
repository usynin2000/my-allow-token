// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract AllowToken {
    string public name = "AllowToken";
    string public symbol = "ATK";
    uint8 public decimals = 18;
    uint256 public totalSupply = 1000 * (10 ** uint256(decimals));

    // Балансы владельцев
    mapping(address => uint256) public balanceOf;

    // allowance[owner][spender] = сколько spender может списать у owner
    mapping(address => mapping(address => uint256)) public allowance;

    constructor() {
        // Все токены изначально у создателя контракта
        balanceOf[msg.sender] = totalSupply;
    }

    // Обычный transfer
    function transfer(address _to, uint256 _amount) public returns (bool success) {
        require(balanceOf[msg.sender] >= _amount, "Not enough tokens");
        balanceOf[msg.sender] -= _amount;
        balanceOf[_to] += _amount;
        return true;
    }

    // Одобрить (approve) spender'у возможность списать до _amount
    function approve(address _spender, uint256 _amount) public returns (bool success) {
        allowance[msg.sender][_spender] = _amount;
        return true;
    }

    // transferFrom списывает токены от owner (from) к to, если хватает allowance
    function transferFrom(address _from, address _to, uint256 _amount) public returns (bool success) {
        require(balanceOf[_from] >= _amount, "Not enough tokens");
        require(allowance[_from][msg.sender] >= _amount, "Not enough allowance");

        balanceOf[_from] -= _amount;
        balanceOf[_to] += _amount;

        allowance[_from][msg.sender] -= _amount;

        return true;
    }
}

contract Bank {
	address private m_owner;
	mapping (string => uint) private m_tokens;
	
	function Bank() public {
		m_owner = msg.sender;
	}
	
	function get_tokens(string token_id) constant public returns(uint) {
		return m_tokens[token_id];
	}
	
	function withdraw(string token_id, uint tokens) public returns(int) {
		if (msg.sender != m_owner)
			return -1;
		else if (tokens > m_tokens[token_id])
			return -2;
		m_tokens[token_id] -= tokens;
		return 0;
	}
	
	function deposit(string token_id, uint tokens) public returns(int) {
		if (msg.sender != m_owner)
			return -1;
		m_tokens[token_id] += tokens;
		return 0;
	}
}

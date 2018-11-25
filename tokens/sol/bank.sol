contract Bank {
	address m_owner;
	mapping (string => uint) m_tokens;
	
	function Bank() public {
		m_owner = msg.sender;
	}
	
	function get_tokens(string token_id) constant returns(uint) {
		return m_tokens[token_id];
	}
	
	function withdraw(string token_id, uint tokens) returns(bool) {
		if (msg.sender != m_owner || tokens > m_tokens[token_id])
			return false;
		m_tokens[token_id] -= tokens;
		return true;
	}
	
	function deposit(string token_id, uint tokens) returns(bool) {
		if (msg.sender != m_owner)
			return false;
		m_tokens[token_id] += tokens;
		return true;
	}
}

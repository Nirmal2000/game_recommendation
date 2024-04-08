from answer_utils import answer_query

class ChatBot:
    def __init__(self, system_message):
        self.messages = [
            {'role': 'system', 'content': system_message}
        ]
        
    def restart(self, ):
        self.messages = []
    
    def ask_question(self, query):
        response = "HI ITS AI"#answer_query(query, self.messages)
        self.messages += [
            {'role': 'user', 'content': query},
            {'role': 'assistant', 'content': response}
        ]
        return self.messages
    


from llm_response_utils import generate_llm_response
import json
import requests
import os
from web_search_utils import get_html_contents, brave_search


def query_decomposition(query):

    sys_prompt = '''Decompose the query given to you into multiple sub-questions. The answers to the sub-questions should collectively provide a comprehensive answer to the original complex question. If the question isn't complex enough just return an array with just the same question.'''
    messages = [
        {'role':'system', 'content': sys_prompt},
        {'role':'user', 'content': '''Query: In the highly anticipated RPG game "Eldoria: Shadow of the Ancients," how does the new dynamic weather system impact gameplay, particularly in terms of character abilities and environmental interactions, and what are the key differences compared to the weather system in its predecessor, "Eldoria: Rise of the Fallen"?'''},
        {'role': 'assistant', 'content': '''```json
{"Decomposed Query": ["What are the main features of the new dynamic weather system in "Eldoria: Shadow of the Ancients"?",  "How do different weather conditions affect character abilities in "Eldoria: Shadow of the Ancients"?", "How does the weather system influence environmental interactions in "Eldoria: Shadow of the Ancients"?", "What are the key differences between the weather systems in "Eldoria: Shadow of the Ancients" and its predecessor, "Eldoria: Rise of the Fallen"?"]}
```'''},
        {'role': 'user', 'content': '''Query: In the multiplayer online battle arena game "Legends of Valoria," how do the latest balance changes affect the viability of support characters in competitive play, and what strategies should players consider adopting to maximize their effectiveness in light of these changes?'''},
        {'role': 'assistant', 'content': '''```json
{"Decomposed Query": ["What are the specific balance changes made to support characters in the latest update of "Legends of Valoria"??", "How have these balance changes impacted the overall meta and role of support characters in competitive play?", "What are the strengths and weaknesses of support characters after the balance changes?", "What strategies or team compositions are emerging as effective for support characters in the current competitive meta?", "How do the balance changes affect the synergy between support characters and other roles in the game?"]}
```'''},
        {'role': 'user', 'content': f'Query: {query}'}
    ]
    results = generate_llm_response(messages)
    return json.loads('\n'.join(results.split('\n')[1:-1]))['Decomposed Query']


def check_valid_search_results(query, search_context):
    prompt = f'''You are an expert in figuring out which links (aka Search Results) must be clicked so you get an answer for a query.
You are given search results for the query: "{query}". Which of the following search result do you think will have the answer for the given query?

{search_context}

Return the output in the following JSON format:
```json
{{"search_results": [array of integers indicating indices]}}
```'''
    messages = [
        {'role':'user', 'content': prompt}
    ]    
    results = generate_llm_response(messages)
    return json.loads('\n'.join(results.split('\n')[1:-1]))


def answer_sub_query(query):
    search_context, urls = brave_search(query)
    valid_search_context_indices = check_valid_search_results(query, search_context)        

    htm_cnt = get_html_contents([urls[i-1] for i in valid_search_context_indices['search_results']])
    if not htm_cnt:
        return ''
    user_prompt = f'''HTML CONTENT: {htm_cnt[0]}

Query: {query}

Follow the below instructions one by one:
1. Read understand the question
2. Look at the HTML CONTENT and answer the Query only using the provided HTML CONTENT.
3. Respond back with an answer that is as long as possible'''
    
    
    messages = [
        {'role':'system', 'content': '''You are expert in answering any kind of questions asked related to just video games. VERY IMPORTANT THING, you must answer any query asked based only on the Search Results given to you.'''},
        {'role': 'user', 'content': user_prompt}
    ]    
    result = generate_llm_response(messages)    
    return result


def answer_query(query, messages):
    sub_queries = query_decomposition(query)
    if str(type(sub_queries)) != "<class 'list'>": sub_queries = [sub_queries]
    
    sub_queries_answers = [answer_sub_query(i) for i in sub_queries]
    sub_qa_str = '\n\n'.join([f'''{i}\n{j}''' for i,j in zip(sub_queries, sub_queries_answers)])
    
    user_prompt = f'''Given the following sub-queries, their respective answers and your previous responses, synthesize an answer to the original query using only the provided information.
    
{sub_qa_str}

Qriginal Query: {query}

Response must be as exhaustive as possible. Try to cover everybit of information from the given sub query and answers.'''
    
    cur_messages = messages + [        
        {'role': 'user', 'content': user_prompt}
    ]
    result = generate_llm_response(cur_messages)    
    return result
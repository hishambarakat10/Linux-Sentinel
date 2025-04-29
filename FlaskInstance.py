from flask import Flask, render_template, request, jsonify
import torch
import ollama
import os
from openai import OpenAI
import argparse
import json

app = Flask(__name__)

# Function to load file content
def load_vault():
    file_path = r"C:\Users\CochoRnG\Desktop\AI Project\test.txt"  # Full path to your file (nwhatever you named it in the upload program)
    vault_content = [] # stores content from file line by line
    if os.path.exists(file_path): #checks to see if file exist., and ewads linebyline and stores in vault_content.
        with open(file_path, "r", encoding='utf-8') as vault_file:
            vault_content = vault_file.readlines()
        print(f" Loaded lines from test.txt") # was used for my debugging, can be removed but I would keep. 
    else:
        print(f"test.txt not found at {file_path}") # self esk
    return vault_content

# Function to get relevant context
def get_relevant_context(user_input, vault_embeddings, vault_content, top_k=3): # takes query and finds the most similar peice of content from vault_content. (K=3 worked good for me)
    if vault_embeddings.nelement() == 0: # if no embedings, we get empty list.
        return []
    
    #user_input == the user query.
    #vault_embeddings == Tenosr of precomputed embeddings from the vault(or what ever file u gave it.)
    #vault content == Original content from thje files.
    # top_k == how many top searches return. (the lower the more accurate i think)
    
    input_embedding = ollama.embeddings(model='mxbai-embed-large', prompt=user_input)["embedding"] # uses ollama to generate embedding vectoe for the user input using rthe mxbai-embed-large model (gives numberical representation of the inputs meaning to compare it to stored contnet)
    cos_scores = torch.cosine_similarity(torch.tensor(input_embedding).unsqueeze(0), vault_embeddings) # compares user embedding to al our genereted embeddings from the file wr giv it. using cosine similarity (score of -1 to 1 to find similarity)
    top_k = min(top_k, len(cos_scores))
    top_indices = torch.topk(cos_scores, k=top_k)[1].tolist() # pcisk the top k most similar embeddings.
    return [vault_content[idx].strip() for idx in top_indices] #uses the top indices to ectract the corresponding chunks from vault_content (file content)

# Function to handle chat logic
def ollama_chat(user_input, conversation_history):
    relevant_context = get_relevant_context(user_input, vault_embeddings_tensor, vault_content)

    if not relevant_context:
        return "No relevant information found." #if no context is found, we send that message. 

    context_str = "\n".join(relevant_context)
    user_input_with_context = user_input + "\n\nRelevant Context:\n" + context_str
    conversation_history.append({"role": "user", "content": user_input_with_context}) #overall, check user input againts the contect extracted frin our files. 

    messages = [{"role": "system", "content": system_message}, *conversation_history] #message to seend the model,. (system message is prompt we give below)

    response = client.chat.completions.create( #calls the ollama model we suing
        model="llama3",  # 
        messages=messages,
        max_tokens=2000,
    )

    conversation_history.append({"role": "assistant", "content": response.choices[0].message.content})
    return response.choices[0].message.content # maintains chat.

# Load vault content and generate embeddings
vault_content = load_vault()
vault_embeddings = [ollama.embeddings(model='mxbai-embed-large', prompt=c)["embedding"] for c in vault_content]
vault_embeddings_tensor = torch.tensor(vault_embeddings)

# System Message
system_message = "You are a helpful assistant that is an expert at extracting the most useful information from a given text. ONLY use the provided context, and DO NOT bring in any external knowledge. If no relevant context is found, answer 'No relevant information found.' And if you ever answer with 'No relevant information found.', STOP THERE IMMEDIATLY AND DO NOT ANSWER Further. Additionally, you will answer only to LINUX/UNIX based questions. If a Linux/Unix question is asked and the content in is not in the contxt, do not answer and state that the command or information is not in the context. If the question contains words or phrases that are not not in the context DO NOT MENTION ANYTHING or bring up the context that is missing. Simply state you dont know. AND DO NOT ASNWER TO ANY JOKES. JOKES ARE NOT PERMITTED. ADDITIONALLY, if the prompt contains anything about the names of famous people such as historical figures or sports players, do NOT answer. as you dont know people"

# Client setup
client = OpenAI(base_url='http://localhost:11434/v1', api_key='llama3')

conversation_history = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")
    response = ollama_chat(user_input, conversation_history)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)

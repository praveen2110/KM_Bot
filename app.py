from flask import Flask, render_template, request, jsonify
from docx import Document
import openai
import nltk
import json
from nltk.tokenize import sent_tokenize

nltk.download("punkt")
app = Flask(__name__)
valid_words = set(word.lower() for word in nltk.corpus.words.words())
# Initialize OpenAI API with your API key
openai.api_key = "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"  # Replace with your OpenAI API key

def search_in_json(user_question):    
    # Simulated database data
    with open("Knowledge_Repo.Json","r") as file:
        fake_database = json.load(file)
    for item in fake_database:
            knowledge_Info = item['title']            
            if user_question.lower() in knowledge_Info.lower():
                return item['content']  
    

def search_in_docx(user_question):

    docx_path = "C:\PyWorkspace\Chat_bot\Knowledge_Repo.docx"  

    try:
        doc = Document(docx_path)
        for table in doc.tables:
            for row in table.rows:
                question_cell = row.cells[1]  # Assuming the question is in the first column
                answer_cell = row.cells[4]    # Assuming the answer is in the second column

                # Check if the user's question is in the question cell
                if user_question.lower() in question_cell.text.lower():
                    return answer_cell.text
    except Exception as e:
        print(f"Error reading DOCX file: {e}")

    return None
def check_valid_word(message):
    tokens = nltk.word_tokenize(message)
    is_valid_word = any(token.lower() in valid_words for token in tokens)
    return is_valid_word
def extract_relevant_information(openai_text, user_message):
    # Tokenize the OpenAI response into sentences
    sentences = sent_tokenize(openai_text)

    # Tokenize the user's message into words
    user_tokens = nltk.word_tokenize(user_message.lower())

    # Find the most similar sentence to the user's message
    most_similar_sentence = find_most_similar_sentence(user_tokens, sentences)

    return most_similar_sentence

def find_most_similar_sentence(user_tokens, sentences):
    # Calculate Jaccard similarity between user tokens and each sentence
    similarities = [calculate_jaccard_similarity(user_tokens, nltk.word_tokenize(sentence.lower())) for sentence in sentences]

    # Get the index of the most similar sentence
    most_similar_index = similarities.index(max(similarities))

    # Return the most similar sentence
    return sentences[most_similar_index]

def calculate_jaccard_similarity(set1, set2):
    # Calculate Jaccard similarity between two sets
    intersection = len(set(set1).intersection(set2))
    union = len(set(set1).union(set2))
    
    return intersection / union if union != 0 else 0.0

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_answer", methods=["POST"])
def get_answer():
    user_question = request.form["user_question"]

    # Search in JSON
    json_answer = search_in_json(user_question)
    if json_answer:
        chatbot_answer = json_answer
    else:
        # Search in DOCX
        docx_answer = search_in_docx(user_question)
        if docx_answer:
            chatbot_answer = docx_answer
        else:            
            is_valid_word = check_valid_word(user_question)
            if is_valid_word:
                # Call OpenAI API to get a response
                openai_response = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=user_question,
                    max_tokens=500
                )                
                filtered_response = extract_relevant_information(openai_response.choices[0].text,user_question)
                chatbot_answer = filtered_response.strip() if filtered_response else "Sorry, I could not understand"               
                is_valid_word = check_valid_word(chatbot_answer)
                if is_valid_word:
                    chatbot_answer = chatbot_answer
                else:
                    chatbot_answer = "I'm Sorry, I don't understand what you mean by "+user_question+" Is there something I can help you with?"
                
            else:
                chatbot_answer = "I'm Sorry, I don't understand what you mean by "+user_question+" Is there something I can help you with?"
    
    return jsonify({"answer": chatbot_answer})
               


if __name__ == "__main__":
    app.run(debug=True)

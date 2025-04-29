import os
import sys
import PyPDF2
import re
import json

def chunk_text(text, chunk_size=1000):
    text = re.sub(r'\s+', ' ', text).strip() # here makes it so there ios no extra white spaces in the code. 
    sentences = re.split(r'(?<=[.!?]) +', text) # This is use dto split the sentence. So "Hello. How are you?" would be split into ["Hello.", "How are you?"]
    chunks = [] # will store the smaller text chuinks we get.
    current_chunk = "" # Will hold the sentences as we process them.
    for sentence in sentences: #loop ofcourse
        if len(current_chunk) + len(sentence) + 1 < chunk_size:   # Checks to see if adding current setnece to current_chunk woull keep it under the specidied chuck size. I have it at 1000 since I was having issues with other numbers. if below 1000, it keep adding!
            current_chunk += (sentence + " ").strip() 
        else: # if sentence is too large, the current chunck is appended to chumnks list. 
            chunks.append(current_chunk)
            current_chunk = sentence + " "  
    if current_chunk: # IMPORTANT! if the loop finishes and any remaining text in current chunk is left behind, it is added to the last chunk. meaning no text is left behind.
        chunks.append(current_chunk)
    return chunks

def convert_pdf_to_text(file_path): 
    with open(file_path, 'rb') as pdf_file: #opens pdf in rb, which is neccisary to process pdf files.
        pdf_reader = PyPDF2.PdfReader(pdf_file) # THIS READS AND EXTRACT CONTENT FROM PDF FILE
        text = '' # stores extracted text hee.
        for page in pdf_reader.pages: # Makes sire to get all pages in pdf. 
            page_text = page.extract_text()
            if page_text: #checks ifpage is empty. 
                text += page_text + " "
    return chunk_text(text) #retuns. 

def process_txt_file(file_path): # opens specified txt file and gets smaller ocntent.
    with open(file_path, 'r', encoding="utf-8") as txt_file:
        text = txt_file.read()
    return chunk_text(text)

def process_json_file(file_path): # opensa json file, converts into strings while still keeping json data. 
    with open(file_path, 'r', encoding="utf-8") as json_file:
        data = json.load(json_file)
    text = json.dumps(data, ensure_ascii=False)
    return chunk_text(text)

def save_chunks_to_file(chunks, output_file="test.txt"): #select where to save it. Here i saved it to test. But remember this name as you will call it with the other code for embeddings.
    with open(output_file, "w", encoding="utf-8") as out_file:
        for chunk in chunks:
            out_file.write(chunk.strip() + "\n")
    print(f"The file has vbeem saved to: {output_file}")

def main():
    if len(sys.argv) < 2:
        print("Please provide a file name after calling python programm.")
        print("Example: python SchoolTestNGUpload.py Test.pdf(file name here)")
        sys.exit(1)

    file_path = sys.argv[1]
    if not os.path.isfile(file_path):
        print(f" File not found, maybe specifiy full path or just name if in same directory: {file_path}")
        sys.exit(1)

    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        chunks = convert_pdf_to_text(file_path)
    elif ext == ".txt":
        chunks = process_txt_file(file_path)
    elif ext == ".json":
        chunks = process_json_file(file_path)
    else:
        print(f" Unsupported file type, amke sure its txt, pdf or json: {ext}")
        sys.exit(1)

    save_chunks_to_file(chunks)

if __name__ == "__main__":
    main()
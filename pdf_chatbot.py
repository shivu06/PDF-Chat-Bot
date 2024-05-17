import PyPDF2
import os
import openai

# Set OpenAI API key (make sure to secure your key)
openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, "rb") as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            detected_text = ""
            for page in pdf_reader.pages:
                detected_text += page.extract_text() or ""
        return detected_text
    except Exception as e:
        print(f"Error reading PDF file: {e}")
        return ""

def continue_chat(system_message, user_assistant_messages):
    system_msg = [{"role": "system", "content": system_message}]
    user_assistant_msgs = [
        {"role": "assistant", "content": user_assistant_messages[i]} if i % 2
        else {"role": "user", "content": user_assistant_messages[i]}
        for i in range(len(user_assistant_messages))
    ]
    all_msgs = system_msg + user_assistant_msgs

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=all_msgs,
            temperature=0.5,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Error in OpenAI API call: {e}")
        return ""

def main():
    pdf_file_path = input('Enter PDF filepath: ')
    if not os.path.isfile(pdf_file_path):
        print("File does not exist. Please check the file path.")
        return

    detected_text = extract_text_from_pdf(pdf_file_path)
    if not detected_text:
        print("No text detected in the PDF or failed to read the PDF.")
        return

    system_msg = "reply from the system."

    while True:
        query = input("PROMPT: ")
        if query.lower() == 'exit':
            break
        user_msg = detected_text + "\n\n" + query
        response = continue_chat(system_msg, [user_msg])
        print(response)

if __name__ == "__main__":
    main()

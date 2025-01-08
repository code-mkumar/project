import requests
import json
import streamlit as st
# LM Studio API endpoint
LM_STUDIO_API_URL = "http://127.0.0.1:1234/v1/chat/completions"

# Function to query LM Studio with streaming
def query_lm_studio(prompt, context):
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": "meta-llama-3.1-8b-instruct",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Context: {context}\n\nQuestion: {prompt}"}
        ],
        "temperature": 0.7,
        "max_tokens": 2000,
        "stream": True  # Enable streaming
    }
    content_accumulated=''
    
    # Stream the response from LM Studio
     # Stream the response from LM Studio
    with requests.post(LM_STUDIO_API_URL, headers=headers, data=json.dumps(payload), stream=True) as response:
        if response.status_code == 200:
            # st.write("Streaming response:")
            with st.chat_message("assistant"):
                content_placeholder = st.empty() 
                for line in response.iter_lines():
                    if line:  # Only process non-empty lines
                        decoded_line = line.decode('utf-8')  # Decode the byte line to a string
                        if decoded_line.startswith('data:'):
                            decoded_line = decoded_line[len('data:'):].strip()  # Remove the 'data:' prefix
                        
                        try:
                            # Parse the JSON content and print it
                            if decoded_line == 'DONE':
                                return
                            json_data = json.loads(decoded_line)
                            response=json.dumps(json_data, indent=2) # Pretty-print the JSON data
                            data = json.loads(response)
                            # Extract content from the response
                            content=''
                            if data['choices'][0]['delta']:
                                content = data['choices'][0]['delta']['content']
                            # st.write("\b",content)
                            
                            if content:  # If content exists, accumulate it
                                content_accumulated += content
                            # Continuously display the accumulated content
                                
                                content_placeholder.markdown(content_accumulated)
                        except json.JSONDecodeError as e:
                            # st.write(f"Error parsing line: {decoded_line}")  # Print the line if it's not valid JSON
                            st.write()
                            # pass
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
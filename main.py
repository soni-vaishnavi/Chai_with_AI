import os
import requests
import json
import schedule
from dotenv import load_dotenv

# --- Step 1: Securely load all API credentials ---
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
hf_access_token = os.getenv("HF_ACCESS_TOKEN")
facebook_token = os.getenv("FACEBOOK_ACCESS_TOKEN")
page_id = os.getenv("FACEBOOK_PAGE_ID")  # Your FB Page ID

print("Starting the automation process...")

# --- Step 2: Manage daily counter ---
def get_next_day():
    counter_file = "day_counter.txt"

    if not os.path.exists(counter_file):
        day = 1
    else:
        with open(counter_file, "r") as f:
            try:
                day = int(f.read().strip()) + 1
            except ValueError:
                day = 1

    with open(counter_file, "w") as f:
        f.write(str(day))

    return day

# --- Step 3: Load next prompt from prompt bank ---
def get_next_prompt():
    prompts_file = "prompts.txt"
    counter_file = "prompt_counter.txt"

    # Example prompts if prompts.txt doesn’t exist
    if not os.path.exists(prompts_file):
        default_prompts = [

"Explain supervised learning with a real-world example in 100 words",
            
"What is underfitting in ML? Explain simply maximum 150 words",

"Explain the difference between classification and regression ",

"What is reinforcement learning? Give a real-world analogy",

"Explain the difference between generative AI and traditional AI in with an easy analogy.",

"What is the Turing Test and does ChatGPT pass it? Explain in a fun way .",

"How does AI detect fake news? Explain simply  with a real-world example.",

"What is a neural network? Explain it like I’m 12 years old ",

"Explain how AI is used in self-driving cars with a simple analogy.",

"What is prompt engineering? Explain with a funny real-life analogy",

"Explain how AI is helping doctors predict diseases before symptoms appear.",

"What is computer vision? Explain with real-life applications.",

"Explain how AI translates languages instantly like Google Translate  .",

"What is bias in AI? Explain with a simple funny example   .",

"How does ChatGPT actually generate answers? Explain simply  with an example.",

"What is reinforcement learning from human feedback (RLHF)? Explain .",

"Explain how AI is being used in Hollywood movies or Netflix recommendations .",

"What is deepfake AI? Explain with a funny but clear example .",

"Explain how AI can create music like a human composer .",

"What is AGI (Artificial General Intelligence)? Explain with a sci-fi twist .",

"Explain how AI helps in fraud detection for banks .",

"What is the difference between machine learning and deep learning? Explain.",

"Explain how AI chatbots are replacing customer service in a fun way .",

"Give 5 surprising and funny facts about AI that most people don’t know."]
        with open(prompts_file, "w") as f:
            f.write("\n".join(default_prompts))

    # Load all prompts
    with open(prompts_file, "r") as f:
        prompts = [line.strip() for line in f if line.strip()]

    # Track which prompt to use
    if not os.path.exists(counter_file):
        idx = 0
    else:
        with open(counter_file, "r") as f:
            try:
                idx = int(f.read().strip())
            except ValueError:
                idx = 0

    # Get prompt and update counter
    prompt = prompts[idx % len(prompts)]
    next_idx = (idx + 1) % len(prompts)  # loops back when list ends
    with open(counter_file, "w") as f:
        f.write(str(next_idx))

    return prompt

# --- Step 4: Generate Post Content ---
def generate_post_content(prompt):
    print("Generating post content from Gemini API...")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_api_key}"
    payload = {"contents": [{"parts": [{"text": f'write the title of this content on the top in bold and italics and then write the content in maximum 100 words{prompt}'}]}]}
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        data = response.json()
        post_text = data['candidates'][0]['content']['parts'][0]['text']
        print("Content generated successfully.")
        return post_text
    except requests.exceptions.RequestException as e:
        print(f"Error generating content from Gemini: {e}")
        return None

# --- Step 5: Generate Image ---
def generate_image(prompt_text, day):
    print("Generating image from Hugging Face API...")
    image_prompt = f"Create a digital art, futuristic illustration to post: {prompt_text}"
    
    HF_MODEL_ID = "stabilityai/stable-diffusion-xl-base-1.0"
    HF_API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL_ID}"
    headers = {"Authorization": f"Bearer {hf_access_token}"}
    payload = {"inputs": image_prompt}
    
    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload)
        response.raise_for_status()

        os.makedirs("images", exist_ok=True)
        image_filename = f"images/generated_image{day}.jpg"
        with open(image_filename, "wb") as f:
            f.write(response.content)
        print(f"Image saved successfully as {image_filename}")
        return image_filename
    except requests.exceptions.RequestException as e:
        print(f"Error generating image: {e}")
        return None

# --- Step 6: Post to Facebook ---
def post_to_facebook(message, image_path):
    print("Posting content to Facebook...")
    url = f"https://graph.facebook.com/v19.0/{page_id}/photos"
    
    try:
        with open(image_path, "rb") as image_file:
            files = {"source": image_file}
            payload = {"caption": message, "access_token": facebook_token}
            response = requests.post(url, data=payload, files=files)
            response.raise_for_status()
        print("Post successful! Check your page.")
        return True
    except Exception as e:
        print(f"Error posting to Facebook: {e}")
        return False

# --- Step 7: Full automation ---
def automatic_post():
    prompt = get_next_prompt()  # Different prompt each day
    post_message = generate_post_content(prompt)
    if post_message:
        day = get_next_day()
        image_file_path = generate_image(post_message, day)
        if image_file_path:
            post_to_facebook(post_message, image_file_path)
            print("Automation completed.\n")
        else:
            print("Image generation failed.")
    else:
        print("Content generation failed.")

# --- Main Scheduler ---
if __name__ == "__main__":
    schedule.every().day.at("17:06").do(automatic_post)
    while True:
        schedule.run_pending()

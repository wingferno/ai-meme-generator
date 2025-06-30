from google import genai
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont
import os
import json

load_dotenv()
with open('meme_templates.json', 'r') as file:
    # Load its content and make a new dictionary
    data = json.load(file)

def get_memes(response):
    start = response.find("```json") + 7
    end = response.rfind("```")
    json_text = response[start:end]
    memes = json.loads(json_text)
    return memes


# Access the API key from environment variables
my_api_key = os.getenv('MY_API_KEY')
client = genai.Client(api_key=my_api_key)
# Get all meme templates titles and write first ai prompt
all_templates = open('output.txt').read()

print("Add as much context as possible for the prompt. ")
user_prompt = input("Write your meme idea here and press enter: ")

ai_prompt_1 = f"""You are a sly meme expert. Your goal is to create the best 3 fitting memes based on the following prompt: {user_prompt}
Now you must choose one unique template for each meme, and here are all the choices (make sure to consider all of them, especially the middle to last ones): {all_templates}
For each meme, make sure you have the right number of text boxes and come up with text for each box. The content in each box should be short and absolutely fit the context of the template.
You must return a dictionary with the following structure:
{{"name of meme 1": ["<text in text box 1>", "<text in text box 2>", ...], "name of meme 2": ["<text in text box 1>", "<text in text box 2>", ...], "name of meme 3": ["<text in text box 1>", "<text in text box 2>", ...], ...}}
Make sure to use the exact names of the templates as they are in the list, and put the text boxes in chronological order in the dictionary list for each meme.
The memes should be witty, bold and fit the common usage of the template. You must be creative and identify the contrast/irony in the prompt to showcase it. Keep it short, simple and clear."""

print("initializing...")
response = client.models.generate_content(
    model="gemini-2.5-flash-preview-05-20", contents=ai_prompt_1
)
try:
    memes = get_memes(response.text) #dictionary
except:
    print("Issue occurred, you need to rerun the code.")
    quit()
# memes = {'Distracted Boyfriend': ['Me actually learning to code', 'My brain', 'Using ChatGPT to cook crazy code'], 'Grus Plan': ['Become a coding prodigy', 'Master multiple programming languages', 'Develop groundbreaking apps to impress friends', "Ask ChatGPT to 'cook crazy code' and claim it's mine"], 'Expanding Brain': ['Knowing basic HTML', 'Copy-pasting from Stack Overflow', 'Using ChatGPT to write simple functions', "Friends calling me a 'pro coder' because ChatGPT built an entire app"]}
print("loading...")
def create_ai_prompt_2():
    draft_prompt = f"""You are a meme expert who knows how to position text boxes in memes such that the text matches the image template and the logical progression/order.
    For each meme, you must analyze the content of each meme and identify the characters or objects, their emotions/expressions and their position relative to the center (left/right up/down). Then, you have to match each individual text box to the correct x,y position such that the text box is well positionned on the image template.
    The x,y positions are given in proportions of the template image size, so for example, if the x,y position is 0.5,0.5, it means the text box is in the center of the image.
    The higher the x value, the more to the right the text box is, and the higher the y value, the closer to the top the text box is.
    Here are the memes you must position the text boxes for: \n"""

    text = ""
    for title in memes:
        text += f"{title}: \n"
        for i in range(len(memes[title])):
            text += f"Text box {i + 1}: {memes[title][i]}\n"
        text += f"Position of text boxes for {title}:\n"
        for j in range(len(memes[title])):
            meme_dictionary = next((item for item in data['memes'] if item.get("title") == title), None)
            try:
                text += f"x:{meme_dictionary['text_boxes'][j]['x']} y:{meme_dictionary['text_boxes'][j]['y']}\n"
            except IndexError:
                text += "missing text box (you need to take out one text in your meme)\n"
        text += "\n"
    #print(text)

    draft_prompt += text
    draft_prompt += """Make sure to get the right position for each text box so that the meme makes sense and follows a logical visual progression.
    You must return a dictionary with the following structure:
    {"name of meme 1": [{"textbox": "content_of_textbox1", "x": value_of_x, "y": value_of_y}, {"textbox": "content_of_textbox2", "x": value_of_x, "y": value_of_y}, ...], "name of meme 2": [{"textbox": "content_of_textbox1", "x": value_of_x, "y": value_of_y}, ...], ...}
    Make sure to use the exact names of the memes and to position the text boxes in the typical way.
    Take into account the content of the template image, especially the characters and their emotions/facial expressions. 
    If Distracted Boyfriend is present, the left most text box is the 'guilty pleasure that attracts you' and the right most is 'the rational choice you avoid'.
    Make sure to respect the progression in quadrants"""
    return draft_prompt

ai_prompt_2 = create_ai_prompt_2()
#print(ai_prompt_2)

response2 = client.models.generate_content(
    model="gemini-2.5-flash-preview-05-20", contents=ai_prompt_2
)
memes = get_memes(response2.text) #dictionary
print("positioning text boxes...")
# print(memes)

#memes = {'Distracted Boyfriend': [{'textbox': 'My brain', 'x': 0.27, 'y': 0.28}, {'textbox': 'Me actually learning to code', 'x': 0.6, 'y': 0.5}, {'textbox': 'Using ChatGPT to cook crazy code', 'x': 0.86, 'y': 0.38}], 'Grus Plan': [{'textbox': 'Become a coding prodigy', 'x': 0.38, 'y': 0.2}, {'textbox': 'Master multiple programming languages', 'x': 0.88, 'y': 0.2}, {'textbox': 'Develop groundbreaking apps to impress friends', 'x': 0.38, 'y': 0.71}, {'textbox': "Ask ChatGPT to 'cook crazy code' and claim it's mine", 'x': 0.88, 'y': 0.7}], 'Expanding Brain': [{'textbox': 'Knowing basic HTML', 'x': 0.24, 'y': 0.88}, {'textbox': 'Copy-pasting from Stack Overflow', 'x': 0.24, 'y': 0.62}, {'textbox': 'Using ChatGPT to write simple functions', 'x': 0.24, 'y': 0.38}, {'textbox': "Friends calling me a 'pro coder' because ChatGPT built an entire app", 'x': 0.24, 'y': 0.14}]}

#Add textbox width and height to each text box in the memes dictionary
for meme_name, text_boxes in memes.items():
    for text_box in text_boxes:
            meme_dictionary = next((item for item in data['memes'] if item.get("title") == meme_name), None)
            if meme_dictionary:
                for box in meme_dictionary['text_boxes']:
                    if box['x'] == text_box['x'] and box['y'] == text_box['y']:
                        text_box['width'] = box['width']
                        text_box['height'] = box['height']

print(memes)

def wrap_text(text, font, draw, max_width):
    lines = []
    words = text.split()
    line = ""
    for word in words:
        test_line = line + word + " "
        width = draw.textlength(test_line, font=font)
        if width <= max_width:
            line = test_line
        else:
            if line:
                lines.append(line.strip())
            line = word + " "
    if line:
        lines.append(line.strip())
    return lines
def draw_text_box(img_path, meme_title, textbox_lst, font_path="impact.ttf"):
    img = Image.open(img_path)
    draw = ImageDraw.Draw(img)
    width, height = img.size


    for textbox in textbox_lst:
        max_width, max_height = textbox['width']*width*0.92, textbox['height']*height*0.92
        x, y = textbox['x']*width, (1-textbox['y'])*height
        font_size = 100

        # Shrink font until text fits the box
        
        while font_size > 10:
            font = ImageFont.truetype(font_path, font_size)
            lines = wrap_text(textbox["textbox"], font, draw, max_width)
            line_height = font.getbbox("Ay")[3] - font.getbbox("Ay")[1]
            total_height = len(lines) * (line_height + 4)
            if total_height < max_height and all(draw.textlength(line, font=font) <= max_width for line in lines):
                break
            font_size -= 1
        
                    
        # Draw each line centered
        text_y = y - total_height // 2
        for line in lines:
            line_width = draw.textlength(line, font=font)
            text_x = x - line_width // 2
            draw.text(
                (text_x, text_y),
                line,
                font=font,
                fill="white",
                stroke_width=font_size*0.1,
                stroke_fill="black"
            )
            text_y += line_height + 4
    img.save(f"{meme_title}.jpg")
    print(f"Saved meme: {meme_title}.jpg")

for meme in memes:
    draw_text_box(f"images/{meme}.jpg", meme, memes[meme])
print("All memes created successfully!")

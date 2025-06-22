from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
from random import randint
import os

# Getting API Key from environmental variable
API_KEY=os.getenv('GEMINI_API_KEY')
IMG_PATH='images/'

def generate_image(prompt):
    '''
    Argument: string, Text prompt
    Result: Generates Image with gemini and stores it as generate_image.jpg

    Uses Gemini to generate an image. If you wish to include an image in your prompt, 
    please add them in images/ directory
    '''
    contents=[prompt]
    images=[]

    try:
        images=os.listdir(IMG_PATH)
    except FileNotFoundError:
        pass

    if images:
        print('Images found, Generating with prompt and image')
        img_name=images[randint(0,len(images)-1)]
        img=Image.open(f'{IMG_PATH}{img_name}')
        contents.append(img)
    else:
        print('No Images found, Generating with only prompt')

    client=genai.Client(api_key=API_KEY)

    response=client.models.generate_content(
        model="gemini-2.0-flash-preview-image-generation",
        contents=contents,
        config=types.GenerateContentConfig(
            response_modalities=['TEXT','IMAGE']
            )
    )

    for part in response.candidates[0].content.parts:
        if part.text is not None:
            with open('generated_text.txt','w',encoding='utf-8') as file:
                file.write(str(part.text))
        elif part.inline_data is not None:
            image=Image.open(BytesIO(part.inline_data.data))
            image.save('generated_image.jpg')

# Example Usage
generate_image('Can you generate a image of steph curry dunking and also generate a cool instagram caption')
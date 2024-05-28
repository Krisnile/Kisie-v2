# -*- coding: utf-8 -*-
'''
@File    :   functions.py
@Time    :   2024/04/30 00:14:44
@Author  :   Krisnile 
@Desc    :   This file stored the functions.
'''


import os
import datetime
import pandas as pd
import gradio as gr
from PIL import Image
from openai import OpenAI
from deep_translator import GoogleTranslator

import prepare as pre
import file_extract as ext


# some variables
visible = False
image = Image.open(pre.Image_Path)
image_w = Image.open(pre.Image_Path_w)
client = OpenAI(base_url=pre.URL, api_key="not-needed")
time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def current_time():
    """
    @description  : Get currnet time
    ----------
    @param  : None
    ----------
    @Returns  : A function contains current time
    ----------
    """

    def helper():
        now = datetime.datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        return f" {current_time}"
    return helper


def image_processing(input_image):
    """
    @description  : give a blank circle around the image
    ----------
    @param  : input_image(path of image input)
    ----------
    @Returns  : new_image(processed)
    ----------
    """
    
    try:
        width, height = input_image.size # get original image's size
        new_width = width + width // 2 # compute the new size
        new_height = height + height // 2
        new_image = Image.new("RGBA", (new_width, new_height), (0, 0, 0, 0)) # create the new image
        
        x_offset = (new_width - width) // 2 # the paste place
        y_offset = (new_height - height) // 2
        new_image.paste(input_image, (x_offset, y_offset)) # paste the place
        return new_image
    except Exception as e:
        print("A exception in image processing occurred.")
        gr.Warning('A exception in image processing occurred.')


def parse_text(text):
    """
    @description  : parse the text and replace special characters in the text
    ----------
    @param  : text(text waiting to parse and replacing special characters)
    ----------
    @Returns  : text(text processed)
    ----------
    @Reference   : https://github.com/THUDM/ChatGLM3 (ChatGLM3/basic_demo/web_demo_gradio.py)
    """
    
    lines = text.split("\n")
    lines = [line for line in lines if line != ""]
    count = 0
    for i, line in enumerate(lines):
        if "```" in line:
            count += 1
            items = line.split('`')
            if count % 2 == 1:
                lines[i] = f'<pre><code class="language-{items[-1]}">'
            else:
                lines[i] = f'<br></code></pre>'
        else:
            if i > 0:
                if count % 2 == 1:
                    line = line.replace("`", "\`")
                    line = line.replace("<", "&lt;")
                    line = line.replace(">", "&gt;")
                    line = line.replace(" ", "&nbsp;")
                    line = line.replace("*", "&ast;")
                    line = line.replace("_", "&lowbar;")
                    line = line.replace("-", "&#45;")
                    line = line.replace(".", "&#46;")
                    line = line.replace("!", "&#33;")
                    line = line.replace("(", "&#40;")
                    line = line.replace(")", "&#41;")
                    line = line.replace("$", "&#36;")
                lines[i] = "<br>" + line
    text = "".join(lines)
    return text


def user(new_input, history_chatbot):
    """
    @description  : add new user's input into the chatbot history
    ----------
    @param  : new_input history_chatbot
    ----------
    @Returns  : an empty strings and updated chatbot history
    ----------
    """
    
    return "", history_chatbot + [[parse_text(new_input), ""]]

def reset_chat(empty_chatbot):
    """
    @description  : reset the prepared dialogue of chatbot
    ----------
    @param  : empty_chatbot
    ----------
    @Returns  : a new chatbot with the prepared dialogue
    ----------
    """
    
    pre.prompt = pre.prompt_set[:]
    return empty_chatbot + [[pre.first_chat[0],pre.first_chat[1]]]

def preview_visible():
    """
    @description  : change the visible of the files' preview
    ----------
    @param  : None
    ----------
    @Returns  : a update of visible
    ----------
    """
    
    global visible
    visible = not visible
    if visible:
        return gr.update(visible=True)
    else:
        return gr.update(visible=False)


def predict(chatbot): 
    """
    @description  : predict the answer
    ----------
    @param  : chatbot with user's input
    ----------
    @Returns  : chatbot with the answer
    ----------
    """
    
    try:
        # print(pre.prompt)
        user_input = ""
        user_input_prompt = ""
        for idx, (user_msg, model_msg) in enumerate(chatbot):
            if idx == len(chatbot) - 1 and not model_msg:
                user_input = user_msg
                user_input_prompt = user_msg
                pre.prompt.append({"role": "user", "content": user_input_prompt}) 

        completion = client.chat.completions.create(  
            model="kisie-model", # Unused  
            messages=pre.prompt,  
            temperature=0.7,  
            stream=True,  
        ) 

        new_message = {"role": "assistant", "content": ""}  
        print("\nReply Check:\n")
        for chunk in completion:  
            if chunk.choices[0].delta.content:  
                print(chunk.choices[0].delta.content, end="", flush=True)  
                new_message["content"] += chunk.choices[0].delta.content  


        chatbot[-1] = [user_input, new_message["content"]]
        pre.prompt.append(new_message)

        return chatbot
    except Exception as e:
        print("A exception in predict occurred.")
        gr.Warning('A exception in predict occurred.')


def empty_his():
    """
    @description  : empty history
    ----------
    @param  : None
    ----------
    @Returns  : None
    ----------
    """
    
    gr.Info('The History Dialogue has been emptied.')
    return None


def translate(original_input):
    """
    @description  : translate any language into English
    ----------
    @param  : text input
    ----------
    @Returns  : text translated
    ----------
    """
    
    try:
        translated = GoogleTranslator(source='auto', target='en').translate(original_input)
        return translated
    except Exception as e:
        print("A exception in translate occurred.")
        gr.Warning('A exception in translate occurred.\nConnecting to a network may solve.')


def save_dialogue(chatbot):
    """
    @description  : save the dualogue locally
    ----------
    @param  : chatbot(which contains the gialogue history)
    ----------
    @Returns  : None
    ----------
    """
    
    try:
        dialogues = {'index': [], 'user messages': [], 'model messages': []}
        index = dialogues['index']
        user_msgs = dialogues['user messages']
        model_msgs = dialogues['model messages']
        for idx, (user_msg, model_msg) in enumerate(chatbot):
            index.append(idx)
            user_msgs.append(user_msg)
            model_msgs.append(model_msg)

        pd.DataFrame(dialogues).to_csv(f'{pre.Save_Dialogue_Path}/chatbot_dialogues_{time}.csv')
        gr.Info(f'The dialogue has been saved to directory: {pre.Save_Dialogue_Path}')
    except Exception as e:
        print("A exception in dialogue saving occurred.")
        gr.Warning('A exception in dialogue saving occurred.')


def text_processing(path_lists_str):
    """
    @description  : extract the character
    ----------
    @param  : file_path
    ----------
    @Returns  : dict of text
    ----------
    """

    try:
        try:
            # print("path_lists_str: ", path_lists_str)
            if path_lists_str == "[]" or path_lists_str == None:
                return path_lists
            # turn string into list
            path_lists = path_lists_str.replace("[","").replace("]","").replace("\'","").split(", ")
            # print("path_lists: ", path_lists)
        except Exception as e:
            print("A exception in str-to-list occurred.")

        try:
            # process list
            file_list = list()
            for file_path in path_lists:
                if file_path.endswith('.pdf') or file_path.endswith('.docx') or file_path.endswith('.png'):
                    file_list.append( os.path.basename(file_path))
            # print("file_list", file_list)
            text_list = ext.batch_extract_text_from_files(path_lists)
            # print("text_list", text_list)
        except Exception as e:
            print("A exception in file&text-list occurred.")

        try:
            text_dict = dict(zip(file_list, text_list))
            print(text_dict)
            return text_dict
        except Exception as e:
            print("A exception in text-dict occurred.")

    except Exception as e:
        print("A exception in text processing occurred.")

def add_file(original_input, add_input):
    """
    @description  : add file content into dialogue
    ----------
    @param  : text input
    ----------
    @Returns  : text with the new added
    ----------
    """
    
    try:
        prompt = pre.add_prompt
        return original_input + prompt + add_input
    except Exception as e:
        print("A exception in add_file occurred.")
        gr.Warning('A exception in add_file occurred.\nConnecting to a network may solve.')
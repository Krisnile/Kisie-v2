# -*- coding: utf-8 -*-
'''
@File    :   webui.py
@Time    :   2024/04/30 00:13:18
@Author  :   Krisnile 
@Desc    :   This file implements a graphical interface.
'''


import gradio as gr
from css import CSS
import prepare as pre
import functions as func


with gr.Blocks(title="Kisie-v2 Board", css=CSS) as demo:
    gr.HTML("""<h1 align="start">Kisie-v2</h1>""")

    with gr.Tab('ChatBot'):
        with gr.Row():
            with gr.Column():
                gr.Image(type="pil", show_label=False, value=func.image_processing(func.image), container=False, show_download_button=False)
                gr.Textbox(show_label=False, value=pre.introduction, lines=17, interactive=False, container=False)
            with gr.Column(scale=4):
                with gr.Row():
                    with gr.Column(scale=8):
                        chatbot = gr.Chatbot(show_label=False, value=[[pre.first_chat[0],pre.first_chat[1]]], container=True, height=520)
                    with gr.Column(scale=3):
                        time = gr.Label(show_label=False, value=func.current_time(), min_width = 100, container=False, every=1)
                        file_explorer = gr.FileExplorer(show_label=False, file_count="multiple", root=pre.File_Explorer_Path, height=380, container=False)
                with gr.Row():
                    with gr.Column(scale=6):
                        user_input = gr.Textbox(label="InputBox", placeholder=pre.hint, lines=7, container=False)
                    with gr.Column(scale=3):
                        with gr.Row():
                            emptyBtn = gr.Button("Clear", min_width=10)
                            saveBtn = gr.Button("Save", min_width=10)
                        with gr.Row():
                            translateBtn = gr.Button("Translate", min_width=10)    
                            scanfileBtn = gr.Button("Scan", min_width=10)
                        with gr.Row():
                            submitBtn = gr.Button("Submit Input")   
                    with gr.Column(scale=2):    
                        file_list = gr.Textbox(label="Path", placeholder="Selected File Path Above",min_width=25, lines=7, container=False)

        with gr.Column(visible=False, elem_classes="modal-box") as preview_box:
            with gr.Row():
                file_list_preview = gr.Textbox(label="Path", placeholder="File Content Below",min_width=40, lines=3)
                close_btn = gr.Button("Close")
            with gr.Row():
                prev_btn = gr.Button("prev-page", visible=False)
                next_btn = gr.Button("next-page", visible=False)  
            with gr.Row():
                file_extract = gr.Textbox(show_label=False, lines=10)
            with gr.Row():
                preview_count = gr.Number(value=0, interactive=False, precision=0, visible=False)
                page_index = gr.Number(value=0, interactive=False, precision=0, visible=False)

    with gr.Tab('Workflow'):
        with gr.Row():
            with gr.Column():
                gr.Image(type="pil", show_label=False, value=func.image_processing(func.image_w), container=False, show_download_button=False)
                gr.Textbox(show_label=False, value=pre.introduction_w, lines=17, interactive=False, container=False)            
            with gr.Column(scale=4):
                with gr.Row():
                    with gr.Column(scale=8):
                        chatbot_w = gr.Chatbot(show_label=False, value=[[pre.first_chat[0],pre.first_chat[1]]], container=True, height=520)              
                with gr.Row():
                    with gr.Column(scale=6):
                        user_input_w = gr.Textbox(label="InputBox", placeholder=pre.hint, lines=7, container=False)
                    with gr.Column(scale=3):
                        with gr.Row():
                            submitBtn_w = gr.Button("Submit Input") 

    
    saveBtn.click(func.save_dialogue, inputs=[chatbot])
    translateBtn.click(func.translate, user_input, user_input)
    close_btn.click(func.preview_visible, outputs=[preview_box], queue=False)
    file_list.change(lambda file_list: file_list, file_list, file_list_preview)
    file_explorer.change(lambda file_explorer: file_explorer, file_explorer, file_list)
    emptyBtn.click(func.empty_his, outputs=[chatbot]).then(func.reset_chat, inputs=[chatbot], outputs=[chatbot])
    submitBtn.click(func.user, [user_input, chatbot], [user_input, chatbot], queue=False).then(func.predict, chatbot, chatbot)
    scanfileBtn.click(func.preview_visible, outputs=[preview_box], queue=False).then(func.text_processing, file_list, file_extract).then(
        func.add_file, inputs=[user_input, file_extract], outputs=[user_input])


if __name__ == "__main__":
    demo.queue()
    demo.launch(server_name="127.0.0.1", server_port=7860, inbrowser=True,share=False)
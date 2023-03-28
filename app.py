import os, sys
import tempfile
import gradio as gr
from modules.text2speech import text2speech 
from modules.sadtalker_test import SadTalker  

def get_driven_audio(audio):  
    if os.path.isfile(audio):
        return audio
    else:
        save_path = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=("." + "wav"),
            )
        gen_audio = text2speech(audio, save_path.name)
        return gen_audio, gen_audio 

def get_source_image(image):   
        return image

def sadtalker_demo(result_dir='./tmp/'):

    sad_talker = SadTalker()
    with gr.Blocks(analytics_enabled=False) as sadtalker_interface:
        gr.Markdown("<div align='center'> <h2> 😭 SadTalker: Learning Realistic 3D Motion Coefficients for Stylized Audio-Driven Single Image Talking Face Animation (CVPR 2023) </span> </h2> \
                    <a style='font-size:18px;color: #efefef' href='https://arxiv.org/abs/2211.12194'>Arxiv</a> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; \
                    <a style='font-size:18px;color: #efefef' href='https://sadtalker.github.io'>Homepage</a>  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; \
                     <a style='font-size:18px;color: #efefef' href='https://github.com/Winfredy/SadTalker'> Github </div>")
        
        with gr.Row().style(equal_height=False):
            with gr.Column(variant='panel'):
                with gr.Tabs(elem_id="sadtalker_source_image"):
                    with gr.TabItem('Upload image'):
                        with gr.Row():
                            source_image = gr.Image(label="Source image", source="upload", type="filepath").style(height=256,width=256)
 
                with gr.Tabs(elem_id="sadtalker_driven_audio"):
                    with gr.TabItem('Upload audio'):
                        with gr.Column(variant='panel'):
                            driven_audio = gr.Audio(label="Input audio", source="upload", type="filepath")
                            # submit_audio_1 = gr.Button('Submit', variant='primary')
                        # submit_audio_1.click(fn=get_driven_audio, inputs=input_audio1, outputs=driven_audio)

        with gr.Row():
            examples = [
                [
                    'examples/source_image/art_10.png',
                    'examples/driven_audio/deyu.wav',
                    True,
                    False
                ]
            ]
            gr.Examples(examples=examples,
                        inputs=[
                            source_image,
                            driven_audio,
                            is_still_mode,
                            enhancer,
                            gr.Textbox(value=result_dir, visible=False)], 
                        outputs=[gen_video, gen_text],
                        fn=sad_talker.test,
                        cache_examples=os.getenv('SYSTEM') == 'spaces')

            with gr.Column(variant='panel'): 
                with gr.Tabs(elem_id="sadtalker_checkbox"):
                    with gr.TabItem('Settings'):
                        with gr.Column(variant='panel'):
                            is_still_mode = gr.Checkbox(label="w/ Still Mode (fewer hand motion)")
                            enhancer = gr.Checkbox(label="w/ GFPGAN as Face enhancer")
                            submit = gr.Button('Generate', elem_id="sadtalker_generate", variant='primary')

                with gr.Tabs(elem_id="sadtalker_genearted"):
                        gen_video = gr.Video(label="Generated video", format="mp4").style(height=256,width=256)
                        gen_text = gr.Textbox(visible=False)


        

        submit.click(
                    fn=sad_talker.test, 
                    inputs=[source_image,
                            driven_audio,
                            is_still_mode,
                            enhancer,
                            gr.Textbox(value=result_dir, visible=False)], 
                    outputs=[gen_video, gen_text]
                    )

    return sadtalker_interface
 

if __name__ == "__main__":

    sadtalker_result_dir = os.path.join('./', 'results')
    demo = sadtalker_demo(sadtalker_result_dir)
    demo.launch()



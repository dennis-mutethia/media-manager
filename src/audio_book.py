
from gtts import gTTS

class AudioBook():
    def __init__(self):
        self.destination_folder = '../data' 
    
    def create(self, input_text_file, output_audio_file):
        # Read the text
        print(f'Reading input file {input_text_file}...')
        with open(input_text_file, 'r', encoding='utf-8') as file:
            text = file.read()
    
        tts = gTTS(text=text, lang='en')
        
        print('Saving Audiobook...')
        tts.save(output_audio_file)
        print(f'Audiobook saved as {output_audio_file}')
    
    def __call__(self):
        input_text_file = f'{self.destination_folder}/LICENSE' 
        output_audio_file = f'{self.destination_folder}/license.mp3'
        self.create(input_text_file, output_audio_file)

AudioBook()()

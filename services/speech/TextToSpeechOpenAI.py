import openai

class TextToSpeechOpenAI:
    def __init__(self, api_key: str, voice="shimmer", model="tts-1"):
        self.__voice = voice  # Доступные: 'alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer'
        self.__model = model  # tts-1, tts-1-hd, gpt-4o-mini-tts
        self.__api_key = api_key
        openai.api_key = self.__api_key

    def createAudio(self, text: str, output_name_file: str):
        if not (isinstance(output_name_file, str) and output_name_file.endswith('.mp3')):
            raise ValueError("The name must be a string and the format is .mp3")

        with openai.audio.speech.with_streaming_response.create(
                model=self.__model,
                voice=self.__voice,
                input=text,
                instructions="Speak in a cheerful and positive tone.",
        ) as response:
            response.stream_to_file(output_name_file)

    def setVoice(self, voice_name: str):
        allowed_voices = ['alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer']
        if voice_name in allowed_voices:
            self.__voice = voice_name
        else:
            raise ValueError(f"Invalid voice name. Choose from {allowed_voices}")

    def setModel(self, model_name: str):
        allowed_models = ['tts-1', 'tts-1-hd']
        if model_name in allowed_models:
            self.__model = model_name
        else:
            raise ValueError(f"Invalid model name. Choose from {allowed_models}")
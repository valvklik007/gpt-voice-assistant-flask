import edge_tts

class TextToSpeechME:
    def __init__(self):
        self.__voice= "ru-RU-DmitryNeural"
        self.__rate = '+20%'
        self.__volume = '+10%'

    async def createAudio(self, text : str, outputNameFile: str):
        if not (isinstance(outputNameFile, str) and outputNameFile.endswith('.mp3')):
            raise ValueError("The name must be a string and the format is .mp3")
        await edge_tts.Communicate(
            text=text,
            receive_timeout=1,
            voice=self.__voice,
            rate=self.__rate,
            volume=self.__volume,
            pitch="+0Hz"
        ).save(outputNameFile)


    def setRate(self, value: str):
        if isinstance(value, str) and value.endswith('%'):
            self.__rate = value
        else:
            raise ValueError("The speed must be a string with a % symbol (eg '+20%')")

    def setVolume(self, value: str):
        if isinstance(value, str) and value.endswith('%'):
            self.__volume = value
        else:
            raise ValueError("Volume must be a string with a % symbol (eg '+10%')")
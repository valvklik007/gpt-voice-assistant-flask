import requests

class SpeechToText:
    def __init__(self, token_key):
        self.__url = "https://api.deepgram.com/v1/listen?language=ru&model=nova-2&smart_format=true"
        self.__token = token_key
        self.__headers = {
            "Authorization": f"Token {self.__token}",
            "Content-Type": "audio/wav"
        }

    def response(self, file : str):
        with open(file, "rb") as f:
            response = requests.post(self.__url, headers=self.__headers, data=f)
        return response

    def responseOnlyText(self, file : str):
        return self.response(file).json()["results"]["channels"][0]["alternatives"][0]["transcript"]

    def __updateHeaders(self):
        self.__headers["Authorization"] = f"Token {self.__token}"

    def setToken(self, token):
        self.__token = token
import openai

class AiAgentGpt:
    def __init__(self, token_key, system_prompt="Ты полезный ассистент"):
        self.__system_prompt = system_prompt
        self.__messages = [{"role": "system", "content": system_prompt}]
        self.__api_key = token_key
        self.__client = openai.OpenAI(api_key=self.__api_key)

    def getMessages(self):
        return self.__messages

    def setStoryManual(self, story_manual):
        self.__messages = story_manual

    def setApiKey(self, api_key):
        self.__api_key = api_key
        self.__client = openai.OpenAI(api_key=self.__api_key)

    def setSystemPrompt(self, system_prompt):
        self.__system_prompt = system_prompt
        for m in self.__messages:
            if m["role"] == "system":
                m["content"] = system_prompt
                break

    def setNewSystemPrompt(self, system_prompt):
        self.__system_prompt = system_prompt
        self.__messages = [{"role": "system", "content": system_prompt}]

    def getMessagesGtp(self, user_input):
        self.__messages.append({"role": "user", "content": user_input})

        response = self.__client.chat.completions.create(
            model="gpt-4o",
            messages=self.__messages,
            temperature=0.7  #креативности
        )

        answer = response.choices[0].message.content
        self.__messages.append({"role": "assistant", "content": answer})
        return answer
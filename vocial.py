from model import LabelModel
from api_filter import TelegramAPI
from chatgptprompts import ChatBot


class Vocial:
    def __init__(self,username=""):
        self.model = LabelModel()
        self.telapi = TelegramAPI()
        self.chatgpt = ChatBot()
        self.username = username

    def main(self,message,testing=False):
        if testing == True:
            message = "what was the average amount of likes i got in the last month?"
            valwewant = self.telapi.response_from_labels("month","average","reactions",self.username)
            response = self.chatgpt.querychatgpt(message,valwewant)
            return response

        modelvals = self.model.main(message)
        valwewant = self.telapi.response_from_labels(modelvals["time"],modelvals["stat"],modelvals["metric"],self.username)
        response = self.chatgpt.querychatgpt(message,valwewant)

        return response

if __name__ == "__main__":
    v = Vocial()
    v.username = "disclosetv"
    res = v.main(message="what posts gave the most reactions in the last month",testing=False)
    print(res)

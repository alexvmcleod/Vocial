from telethon.sync import TelegramClient
from datetime import datetime, timedelta
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
import json
import pytz
import statistics
from urllib.request import urlopen

class TelegramAPI:
    def __init__(self):
        with open('api_keys.json') as f:
            keys = json.load(f)

            self.api_id = keys['api_id']
            self.api_hash = keys['api_hash']
            self.bot_token = keys['bot_token']

    def get_all_messages(self,username):
        einelist = []
        with TelegramClient('test', self.api_id, self.api_hash) as client:
            
            #offset_date=lastweekcutoff
            for message in client.iter_messages(username,reverse=False):
                #finds all reaction types and converts it to likes
                einelist.append(message)
                #print(type(message.date))
            #print(len(einelist))
        return einelist

    def filter_timeframe(self,einelist, timeframe):
        now = datetime.now(pytz.timezone('US/Eastern'))

        timeframes = {
            'hour': timedelta(hours=1),
            'day': timedelta(days=1),
            'week': timedelta(weeks=1),
            'month': timedelta(days=30),  # Approximate one month
            'year': timedelta(days=365),
            'recent': timedelta.max
        }

        if timeframe not in timeframes:
            raise ValueError(f"Invalid timeframe '{timeframe}', should be one of {list(timeframes.keys())}")

        if timeframe == 'recent':
            most_recent_item = max(einelist, key=lambda item: getattr(item, "date"))
            return [most_recent_item]

        start_time = now - timeframes[timeframe]

        return [item for item in einelist if getattr(item, "date") >= start_time]

    def filter_metric(self,einelist,metric,username=""):
        timeframes = {
            'reactions': [],
            'comments': [],
            'forwards': [],
            'views': [],
        }
        for message in einelist:
            reactions,comments,forwards,views = 0,0,0,0
            if message.reactions != None:
                messagereactions = message.reactions.results
                for reacttype in messagereactions:
                    # print(reacttype.reaction)
                    # print(reacttype.count)
                    reactions += int(reacttype.count)
            
            try:
                if message.views != None:
                    views += int(message.views)
            except:print("L")
            try:
                if message.forwards != None:
                    forwards += int(message.forwards)
            except:print("L")

            if message.replies != None:
                comments += int(message.replies.replies)

            timeframes['reactions'].append(reactions)
            timeframes['comments'].append(comments)
            timeframes['forwards'].append(forwards)
            timeframes['views'].append(views)

        return timeframes[metric]

    def filter_stat(self,metriclist,stat):
        if stat=="top":
            return max(metriclist)
        elif stat=="bottom":
            return min(metriclist)
        elif stat=="average":
            return statistics.mean(metriclist)
        elif stat=="median":
            statistics.median(metriclist)
        else:
            return -1

    def response_from_labels(self,timeframe,stat,metric,user):
        fullacountlist = self.get_all_messages(user)
        timefilteredlist = self.filter_timeframe(fullacountlist,timeframe)
        metricfilteredlist = self.filter_metric(timefilteredlist,metric)
        wantedstat = self.filter_stat(metricfilteredlist,stat)
        return wantedstat

    def get_follower_count(self,username):
        url =f"https://api.telegram.org/bot{self.bot_token}/getChatMembersCount?chat_id=@{username}"
        with urlopen(url) as f:
            resp = json.load(f)

        return int(resp['result'])






if __name__ == "__main__":
    pass
    # t = TelegramAPI()
    # einelist = t.get_all_messages("")
    # filteredlist = filter_timeframe(einelist,"day")
    # print(filteredlist)
    # print(len(filteredlist))


    # print(filter_metric(filteredlist,"comments"))
    # print(response_from_labels("recent","top","comments","disclosetv"))

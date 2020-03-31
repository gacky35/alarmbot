from slacker import Slacker
from time import sleep
import settings

def main():
    slack = Slacker(settings.AP)
    slack.chat.post_message("alarm", "Get Up !!")
    history = slack.channels.history("C010Q9041PV")
    ts = history.body["messages"][0]["ts"]
    while True:
        history = slack.channels.history("C010Q9041PV", count=100000, oldest=ts)
        users = [message["user"] for message in history.body["messages"]]
        not_bot = [user for user in users if user != "U010RMZ517T"]
        if len(not_bot):
            break
        else:
            slack.chat.post_message("alarm", "Get Up !!")
    history = slack.channels.history("C010Q9041PV", count=10000, oldest=ts)
    ts_list = [message["ts"] for message in history.body["messages"] if message["user"] == "U010RMZ517T"]
    ts_list.append(ts)
    for ts in ts_list:
        slack.chat.delete("C010Q9041PV", ts=ts, as_user=True)
    slack.chat.post_message("alarm", "Good Morning")

if __name__ == "__main__":
    main()

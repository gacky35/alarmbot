from slacker import Slacker
from time import sleep
import settings

def get_up_time(t):
    with open("./ranking.txt", "r", encoding="utf-8") as f:
        rank = f.read().split()
        rank.append(t)
        rank = sorted(rank)
        slack.chat.post_message("alarm", "ランキング")
        for i, ts in enumerate(rank[:len(rank)-1 if len(rank) > 3 else len(rank)], 1):
            slack.chat.post_message("alarm", i + ". " + ts)
        slack.chat.post_message("alarm", "今回のタイム\n" + t)
        if rank.index(t) < 3:
            slack.chat.post_message("alarm", "更新！" + (rank.index(t) + 1) + "位")
    with open("./ranking.txt", "w") as f:
        f.write("\n".join(rank[:len(rank)-1 if len(rank) > 3 else len(rank)]))

def main():
    slack = Slacker(settings.ACCESS_TOKEN)
    channel_id = settings.CHANNEL_ID
    slack.chat.post_message("alarm", "Get Up !!") #指定の時間に実施する最初の通知
    history = slack.channels.history(channel_id)
    start_ts = history.body["messages"][0]["ts"] #最初の通知時間を取得
    while True:
        sleep(1)
        history = slack.channels.history(channel_id, count=100000, oldest=start_ts) #最新のものから最初の通知まで最大1万件のメッセージを取得
        not_bot_users = [message["user"] for message in history.body["messages"] if 'bot_id' not in message] #取得したメッセージの投稿者を取得
        #not_bot = [user for user in users if user != "U010RMZ517T"] #メッセージ投稿を実施したbot以外のユーザを取得
        if len(not_bot_users):
            break #botユーザ以外からのメッセージがあるとループを抜ける
        else:
            slack.chat.post_message("alarm", "Get Up !!") #botからの投稿しかなかった場合メッセージを投稿
    history = slack.channels.history(channel_id, count=10000, oldest=start_ts)
    get_up_ts = [message["ts"] for message in history.body["messages"] if message["user"] != "U010RMZ517T"] #メッセージ投稿を止めるまでのbotのメッセージ投稿のタイムスタンプを取得
    ts_list = [message["ts"] for message in history.body["messages"] if 'bot_id' in message] #メッセージ投稿を止めるまでのbotのメッセージ投稿のタイムスタンプを取得
    ts_list.append(start_ts)
    for ts in ts_list:
        slack.chat.delete(channel_id, ts=ts, as_user=True) #botの投稿を削除する
    slack.chat.post_message("alarm", "Good Morning")
    t = float(get_up_ts[0]) - float(start_ts)
    with open("./ranking.txt", "r", encoding="utf-8") as f:
        rank = f.read().split()
        rank.append(t)
        rank = list(map(float, rank))
        rank = sorted(rank)
        slack.chat.post_message("alarm", "ランキング")
        for i, ts in enumerate(rank[:len(rank)-1 if len(rank) > 3 else len(rank)], 1):
            slack.chat.post_message("alarm", "{0}. {1}".format(i, ts))
        slack.chat.post_message("alarm", "今回のタイム\n{0}".format(t))
        if rank.index(t) < 3:
            slack.chat.post_message("alarm", "更新！{0}位".format(rank.index(t) + 1))
    with open("./ranking.txt", "w") as f:
        f.write("\n".join(map(str, rank[:len(rank)-1 if len(rank) > 3 else len(rank)])))

if __name__ == "__main__":
    main()

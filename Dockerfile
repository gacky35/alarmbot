FROM python:latest

LABEL maintainer="tgacky, s17t258@stu.kgawa-u.ac.jp"

#ファイルをルートディレクトリに追加
COPY . /

#ルートディレクトリ設定
WORKDIR /

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#コマンド実行
CMD ["python", "cron.py"]

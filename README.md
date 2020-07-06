
# telegram gcloner

一个Telegram机器人，方便手动保存Google Drive资源。如果你有好的想法，欢迎PR。

演示机器人：http://t.me/ahzhebot

## 使用方法

### 准备工作

1. 安装 [Python 3.7+（推荐最新版3.8）](https://www.python.org/downloads/)
2. 下载 [gclone](https://github.com/donwa/gclone/releases) 或者 [fclone（推荐）](https://github.com/mawaya/rclone/releases)
3. 自行熟悉gclone，并获得包含Service Accounts身份信息的json，确认已可以使用`gclone`或者`fclone`进行相关操作
4. 申请一个[Telegram Bot](https://core.telegram.org/bots#6-botfather)，并取得 **token**
5. 获取自己的Telegram ID，比如通过[这个机器人](https://t.me/userinfobot)

### 安装

下载Zip版本或者通过git clone下载
```
$ git clone https://github.com/wrenfairbank/telegram_gcloner
```
通过requirements.txt安装依赖
```
$ pip3 install -r requirements.txt
```
复制`config.ini.example`并更名为`config.ini`
修改对应的内容，包括：

> path_to_gclone = gclone.exe路径（Linux各发行版如通过安装的方式获取，可不填。Win如已加入path亦可不填。fclone一律需要填写）
>
> telegram_token = telegram机器人token
>
> user_ids = 你的telegram id（多个以英文逗号隔开，第一个ID为管理员）
>
> gclone_para_override = 如果你不知道这个是什么就留空

如有兴趣可调整`./utils/restricted.py`里的权限，默认为只回应`user_ids`里的用户

## 运行

1. 运行`telegram_gcloner.py`。
2. 向机器人上传包含SA的ZIP文件，并在信息标题填写`/sa`。
   - 手机用户可先上传ZIP文件，再回复该信息`/sa`。
3. 向机器人发送`/folders`设定常用文件夹。
4. 向机器人发送或转发带有Google Drive链接的信息，按提示操作。

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details


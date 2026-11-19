## B站 爬虫

### 初始化

```
git clone --single-branch --branch main git@github.com:songzy12/bilibili-crawler.git

cd bilibili-crawler
git clone --single-branch --branch output git@github.com:songzy12/bilibili-crawler.git output
```

### 功能1：给定用户 MID，爬取其动态下的所有图片，并发布日期保存至相应的文件夹内。

示例：https://space.bilibili.com/34579852/dynamic

运行：

将 `config_example/` 中的示例文件复制到 `config/`，然后填写：

1. `cookie.txt`：将浏览器开发者工具网络请求头中的 Cookie 粘贴为一行。不要提交或分享此文件。
2. `user_ids.txt`：每行填写一个用户 MID，可在用户主页 URL 中找到。可在 MID 后使用 `#` 添加用户备注；空行和以 `#` 开头的整行注释会被忽略。例如：

```
34579852 # 示例用户
12345678 # 另一位用户
# 这是整行注释
```

3. `flags.txt`：填写运行参数，每行一个参数，带值的参数使用 `--参数=值` 格式。例如：

```
--cookie-file=config/cookie.txt
--user-ids-file=config/user_ids.txt
--output-dir=~/Data/weibo
```

文件中的相对路径以当前工作目录为准。文件不会进行 shell 展开；`--output-dir` 支持 `~`。

在仓库根目录运行：

```
python -m dynamic @config/flags.txt
```

也可使用 `./run.sh`。仍可直接传入参数：

```
python -m dynamic --cookie-file config/cookie.txt --user-ids-file config/user_ids.txt
```

也可通过参数指定其他文件路径。每个用户的数据会分别保存在 `output/dynamic/<MID>/` 下。

可通过 `--output-dir` 指定其他输出目录，例如：

```
python -m dynamic --cookie-file config/cookie.txt --user-ids-file config/user_ids.txt --output-dir ~/Data/weibo
```

此时数据保存在 `~/Data/weibo/dynamic/<MID>/` 下；不指定时仍使用 `output/`。

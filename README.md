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

在 `dynamic` 文件夹下创建两个文件：

1. `cookie.txt`：将浏览器开发者工具网络请求头中的 Cookie 粘贴为一行。不要提交或分享此文件。
2. `user_ids.txt`：每行填写一个用户 MID，可在用户主页 URL 中找到。可在 MID 后使用 `#` 添加用户备注；空行和以 `#` 开头的整行注释会被忽略。例如：

```
34579852 # 示例用户
12345678 # 另一位用户
# 这是整行注释
```

```
python -m dynamic --cookie-file dynamic/cookie.txt --user-ids-file dynamic/user_ids.txt
```

也可通过参数指定其他文件路径。每个用户的数据会分别保存在 `output/dynamic/<MID>/` 下。

import random
import string

def generate_random_code():
    characters = string.ascii_uppercase + string.digits
    random_code = ''.join(random.choice(characters) for _ in range(6))
    return random_code

def domain_split(input_string:str,port:int):
    parts = input_string.split(":")
    if len(parts) == 2:
        return parts[0], int(parts[1])
    elif len(parts) == 1:
        return parts[0], port
    else:
        return None

index = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>验证码邮件</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #0d0d0d; /* 深色背景 */
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }

        .container {
            background-color: #222; /* 略深的灰色背景 */
            border-radius: 16px;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.7); /* 中等强度的阴影效果 */
            padding: 20px;
            text-align: center;
            color: #ffcc00; /* 亮黄色文字 */
        }

        h1 {
            font-size: 24px;
            margin-bottom: 20px;
            color: #eee; /* 橙色标题文字 */
            text-transform: uppercase; /* 转换为大写字母 */
        }

        p {
            font-size: 36px;
            font-weight: bold;
            margin: 0;
            color: #ff5722; /* 橙色验证码文字 */
        }

        .note {
            font-size: 16px;
            margin-top: 20px;
            color: #ccc; /* 淡灰色提示文字 */
        }

        .security-note {
            font-size: 18px;
            color: #ffcc00; /* 亮黄色安全提示文字 */
            margin-top: 20px;
        }

        a {
            color: #ffcc00;
            text-decoration: none;
            font-weight: bold;
        }

        a:hover {
            color: #ff5722; /* 橙色链接文字 */
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>您的验证码是：</h1>
        <p>{{verification_code}}</p>
        <p class="note">本验证码邮件由 EVCode 验证码程序发出，请不要回复。</p>
        <p class="security-note">为了保护您的帐户安全，请勿分享此验证码给任何人。</p>
        <p class="note">查看项目详情：<a href="http://github.com/lidongxun967/EVCode">GitHub项目链接</a></p>
        <p class="note">如果邮件在垃圾箱中，请手动移出，以防下次接收失败。</p>
    </div>
</body>
</html>
"""
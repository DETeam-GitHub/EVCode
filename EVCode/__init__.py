name = "EVCode"

import smtplib
import imaplib
import poplib
import email.message
import EVCLib
from warnings import warn

def check_encryption_mode(server, port, protocol):

    if protocol == "SMTP":
        if port == 25:  return 0
        elif port == 465:   return 1
        elif port == 587:   return 2
    elif protocol == "IMAP":
        if port == 993: return 1
    elif protocol == "POP3":
        if port == 995: return 1
        
    try:
        if protocol == 'SMTP':
            server = smtplib.SMTP(server, port)
            server.starttls()
        elif protocol == 'POP3':
            server = poplib.POP3(server, port)
            server.stls()
        elif protocol == 'IMAP':
            server = imaplib.IMAP4(server, port)
            server.starttls()
        server.quit()
        return 2
    except :
        pass
    
    try:
        if protocol == 'SMTP':
            server = smtplib.SMTP(server, port)
        elif protocol == 'POP3':
            server = poplib.POP3(server, port)
        elif protocol == 'IMAP':
            server = imaplib.IMAP4(server, port)
        server.quit()
        return 0
    except :
        pass

    try:
        if protocol == 'SMTP':
            server = smtplib.SMTP_SSL(server, port)
        elif protocol == 'POP3':
            server = poplib.POP3_SSL(server, port)
        elif protocol == 'IMAP':
            server = imaplib.IMAP4_SSL(server, port)
        server.quit()
        return 1
    except :
        pass


    return -1

def server_link(server, port, protocol, encryption):
    if encryption == 0:
        if protocol == 'SMTP':
            server = smtplib.SMTP(server, port)
        elif protocol == 'POP3':
            server = poplib.POP3(server, port)
        elif protocol == 'IMAP':
            server = imaplib.IMAP4(server, port)
        return server


    elif encryption == 1:
        if protocol == 'SMTP':
            server = smtplib.SMTP_SSL(server, port)
        elif protocol == 'POP3':
            server = poplib.POP3_SSL(server, port)
        elif protocol == 'IMAP':
            server = imaplib.IMAP4_SSL(server, port)
        return server

    elif encryption == 2:
        if protocol == 'SMTP':
            server = smtplib.SMTP(server, port)
            server.starttls()
        elif protocol == 'POP3':
            server = poplib.POP3(server, port)
            server.stls()
        elif protocol == 'IMAP':
            server = imaplib.IMAP4(server, port)
            server.starttls()
        return server

class EVCode():
    def __init__(self,smtp_server,address,password,*
                 ,subject="EVCode 验证码",nickname="EVCode"
                 ,imap_server=None,pop_server=None
                 ,clear_record=True,captcha_page=EVCLib.index,no_warn=False
                 ,code_interpolation="",random_func=EVCLib.generate_random_code):
        
        self.smtp_domain,self.smtp_port = EVCLib.domain_split(smtp_server,587)
        self.smtp_encryption = check_encryption_mode(self.smtp_domain,self.smtp_port,"SMTP")

        if not self.smtp_encryption and not no_warn:
            warn("SMTP No Encryption Warning")
        if imap_server:
            self.imap_domain,self.imap_port = EVCLib.domain_split(imap_server,993)
            self.imap_encryption = check_encryption_mode(self.imap_domain,self.imap_port,"IMAP")
            if not self.imap_encryption and not no_warn:
                warn("IMAP No Encryption Warning")
        else:
            clear_record = False
            
        if pop_server:
            self.pop_domain,self.pop_port = EVCLib.domain_split(pop_server,995)
            self.pop_encryption = check_encryption_mode(self.pop_domain,self.pop_port,"POP3")
            if not self.pop_encryption and not no_warn:
                warn("POP3 No Encryption Warning")
        
        self.index=captcha_page
        self.clear_record=clear_record
        self.send_email_address = address
        self.send_email_password = password
        self.captcha_random_func = random_func
        self.send_email_subject = subject
        self.send_email_nickname = nickname
        self.no_warn = no_warn
        self.code_interpolation = code_interpolation
    def delete_email_inbox(self):
        # 连接到 POP3 服务器
        try:
            mailbox = server_link(self.pop_domain,self.pop_port,"POP3",self.pop_encryption)
            mailbox.user(self.send_email_address)
            mailbox.pass_(self.send_email_password)

            # 获取邮箱中的邮件数量
            num_messages = len(mailbox.list()[1])

            # 删除所有邮件
            for i in range(num_messages):
                mailbox.dele(i + 1)

            # 退出并关闭连接
            mailbox.quit()
        
        except Exception as e:
            if not self.no_warn:
                warn(e)
            return None
        
        return num_messages
    
    def delete_email_records(self,all=True):
        
            # 使用IMAP连接邮箱并删除已发送邮件
            imap_conn = server_link(self.imap_domain,self.imap_port,"IMAP",self.imap_encryption)
            imap_conn.login(self.send_email_address, self.send_email_password)
            imap_conn.select('Sent')  # 进入已发送邮件文件夹

            # 获取已发送邮件的UID
            result, data = imap_conn.uid('search', None, 'ALL')
            if result == 'OK':
                if all:
                    for i in data[0].split():
                        imap_conn.uid('store', i, '+FLAGS', '(\\Deleted)')
                else:
                    imap_conn.uid('store', data[0].split()[-1], '+FLAGS', '(\\Deleted)')
                imap_conn.expunge()
            imap_conn.logout()

    def send_verification_code(self,received_email):
        try:
            # 生成验证码
            verification_code = self.captcha_random_func()

            html_content = self.index

            # 加入插值
            verification_code_interpolation,interpolation = EVCLib.insert_random_between(verification_code,self.code_interpolation)

            # 替换HTML内容中的验证码占位符
            html_content = html_content.replace('{{verification_code}}', verification_code_interpolation)

            # 创建邮件对象
            msg = email.message.EmailMessage()
            msg.add_alternative(html_content, subtype='html')
            msg['Subject'] = self.send_email_subject
            msg['From'] = self.send_email_nickname + ' <' + self.send_email_address + '>'
            msg['To'] = received_email

            # 连接SMTP服务器并发送邮件

            with server_link(self.smtp_domain,self.smtp_port,"SMTP",self.smtp_encryption) as server:
                server.login(self.send_email_address, self.send_email_password)
                server.send_message(msg)
            
            if self.clear_record:
                self.delete_email_records(False)
            if interpolation:
                return verification_code,interpolation
            return verification_code
        except Exception as e:
            if not self.no_warn:
                warn(e)
            return None
        
def About():
    print(r'''About EVCode:
    _______    ________          __   
   / ____/ |  / / ____/___  ____/ /__ 
  / __/  | | / / /   / __ \/ __  / _ \
 / /___  | |/ / /___/ /_/ / /_/ /  __/
/_____/  |___/\____/\____/\____/\___/ 

欢迎使用本库！以下是本库信息：

EVCode采用GNU Lesser General Public License v3 (LGPLv3)许可证。

Wiki页面：https://github.com/lidongxun967/EVCode/wiki
项目页面：https://github.com/DETeam-GitHub/EVCode
包发布页面：https://pypi.org/project/EVCode

作者：DETeam的各位成员们，感谢他们！
''')

if __name__ == "__main__":
    print("建议通过 import EVCode 使用此库，直接运行会触发About！")
    About()
import smtplib
import email.message
import EVCLib
import imaplib
from warnings import warn

class EVCode():
    def __init__(self,smtp_server,address,password,*
                 ,subject="EVCode验证码",nickname="EVCode",imap_server=None,imap_ssl=True,captcha_page=EVCLib.index,random_func=EVCLib.generate_random_code):
        self.index=captcha_page
        self.smtp_domain,self.smtp_port = EVCLib.domain_split(smtp_server,587)
        self.send_email_address = address
        self.send_email_password = password
        self.captcha_random_func = random_func
        self.send_email_subject = subject
        self.send_email_nickname = nickname
        
        if imap_server:
            self.imap_domain,self.imap_port = EVCLib.domain_split(imap_server,993)
            if self.imap_port == 993:
                self.imap_ssl = True
            elif self.imap_port == 143:
                self.imap_ssl = False
            else:
                self.imap_ssl = imap_ssl
            if not self.imap_ssl:   warn("IMAP No SSL Warning")
            self.clear_record = True
        else:
            self.clear_record = False
    
    def delete_email_records(self):
        
            # 使用IMAP连接邮箱并删除已发送邮件
            if self.imap_ssl:
                imap_conn = imaplib.IMAP4_SSL(self.imap_domain, self.imap_port)
            else:
                imap_conn = imaplib.IMAP4(self.imap_domain, self.imap_port)
            imap_conn.login(self.send_email_address, self.send_email_password)
            imap_conn.select('Sent')  # 进入已发送邮件文件夹

            # 获取已发送邮件的UID
            result, data = imap_conn.uid('search', None, 'ALL')
            if result == 'OK':
                imap_conn.uid('store', data[0].split()[-1], '+FLAGS', '(\Deleted)')
                imap_conn.expunge()
            imap_conn.logout()

    def send_verification_code(self,received_email):
        # 生成验证码
        verification_code = self.captcha_random_func()

        html_content = self.index

        # 替换HTML内容中的验证码占位符
        html_content = html_content.replace('{{verification_code}}', verification_code)

        # 创建邮件对象
        msg = email.message.EmailMessage()
        msg.add_alternative(html_content, subtype='html')
        msg['Subject'] = self.send_email_subject
        msg['From'] = self.send_email_nickname + ' <' + self.send_email_address + '>'
        msg['To'] = received_email

        # 连接SMTP服务器并发送邮件
        try:
            with smtplib.SMTP(self.smtp_domain, self.smtp_port) as server:
                server.starttls()
                server.login(self.send_email_address, self.send_email_password)
                server.send_message(msg)
            
            if self.clear_record:
                self.delete_email_records()
            
            return verification_code
        except Exception as e:
            warn(e)
            return None
        

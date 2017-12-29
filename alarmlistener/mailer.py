import logging
from datetime import datetime
from email.message import EmailMessage
from smtplib import SMTP_SSL, SMTPException

__author__ = 'Miel Donkers <miel.donkers@gmail.com>'

log = logging.getLogger(__name__)


class Mailer:
    last_mail_timestamp = datetime.min

    def __init__(self, mail_backoff_timeout_in_sec, smtp_address, smtp_user, smtp_password, mail_from_address, mail_to_address):
        self.backoff_timeout_in_sec = mail_backoff_timeout_in_sec
        self.smtp_address = smtp_address
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        self.mail_from_address = mail_from_address
        self.mail_to_address = mail_to_address

    def sendMail(self, message):
        if (datetime.utcnow() - Mailer.last_mail_timestamp).total_seconds() < self.backoff_timeout_in_sec:
            log.warning('Not mailing, recently already sent a mail')
            return

        log.info('Trying to send mail with message: {}'.format(str(message)))
        try:
            with SMTP_SSL(self.smtp_address) as smtp:
                Mailer.last_mail_timestamp = datetime.utcnow()
                # smtp.set_debuglevel(2)
                smtp.login(self.smtp_user, self.smtp_password)

                msg = EmailMessage()
                msg.set_content('Alarm notification!\nSome unexpected event:\n\n{}'.format(str(message)))
                msg['Subject'] = 'ALARM NOTIFICATION!'
                msg['From'] = self.mail_from_address
                msg['To'] = self.mail_to_address

                smtp.send_message(msg)
        except SMTPException:
            log.exception('Failed to send email!')

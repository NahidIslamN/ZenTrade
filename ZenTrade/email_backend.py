import smtplib
import ssl
from django.core.mail.backends.smtp import EmailBackend

class SSLIgnoreEmailBackend(EmailBackend):
    def _get_connection(self):
        self.connection = smtplib.SMTP(self.host, self.port)
        self.connection.ehlo()
        if self.use_tls:
            # Disable SSL certificate verification
            context = ssl._create_unverified_context()
            self.connection.starttls(context=context)
            self.connection.ehlo()
        if self.username and self.password:
            self.connection.login(self.username, self.password)
        return self.connection

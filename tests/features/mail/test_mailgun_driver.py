from tests import TestCase
from src.masonite.mail import Mailable
import os


class Welcome(Mailable):
    def build(self):
        return (
            self.to("idmann509@gmail.com")
            .subject("Masonite 4")
            .from_("joe@masoniteproject.com")
            .text("Hello from Masonite!")
            .html("<h1>Hello from Masonite!</h1>")
        )


class TestMailgunDriver(TestCase):
    def test_send_mailable(self):
        if os.getenv("RUN_MAIL") == "True":
            # self.application.make("mail").driver("mailgun").mailable(Welcome()).send()
            self.application.make("mail").mailable(
                Welcome().attach("invoice", "tests/integrations/storage/invoice.pdf")
            )
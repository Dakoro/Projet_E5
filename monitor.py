import logging as log
import os
import sys

import psutil
import schedule
import time
from logging.handlers import SMTPHandler
from dotenv import load_dotenv
load_dotenv()

log.basicConfig(filename='logs/metrics.log', level=log.INFO)

SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = os.getenv('SMTP_PORT')
SMTP_USERNAME = os.getenv('SMTP_USERNAME')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
EMAIL_RECEIVER = os.getenv('EMAIL_RECEIVER')


def mk_email_logger():
    smtp_handler = SMTPHandler(
        mailhost=(SMTP_SERVER, SMTP_PORT),
        fromaddr=SMTP_USERNAME,
        toaddrs=EMAIL_RECEIVER,
        subject='Critical RAM Status',
        credentials=(SMTP_USERNAME, SMTP_PASSWORD),
        secure=(),
    )
    logger = log.getLogger('Email Logger')
    logger.addHandler(smtp_handler)
    logger.setLevel(log.CRITICAL)
    return logger


email_logger = mk_email_logger()


def monitor_pdf2img():
    mem = psutil.virtual_memory()
    print(mem[2], type(mem[2]))
    if mem[2] > 50:
        log.critical('RAM exceed 50%\nThe server will be shutdown')
        os.system('pkill -f app.py')
        email_logger.critical('RAM exceed 50%\nThe server will be shutdown')
        sys.exit()
    log.info(mem)


if __name__ == '__main__':
    schedule.every(10).seconds.do(monitor_pdf2img)
    while 1:
        schedule.run_pending()
        time.sleep(1)

import os
import logging
from chalice import Chalice, Response, BadRequestError
from chalicelib import aws_functions
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

# logger 設定
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Chalice 設定
app = Chalice(app_name='linebot-translation')

# LINE Bot API 設定
line_bot_api = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['CHANNEL_SECRET_TOKEN'])


@app.route('/translation', methods=['POST'])
def controller():
    logger.info('CALLED: controller()')

    # get X-Line-signature header value
    request     = app.current_request
    signature   = request.headers['X-Line-Signature']

    # get request body as text
    body        = request.raw_body.decode('utf8')
    logger.info(f'REQUEST_BODY: {body}')

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        raise BadRequestError('InvalidSignatureError')

    return Response(body='Executed', status_code=200)


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    logger.info('CALLED: handle_message()')

    # get message.text
    received_text = event.message.text
    logger.info(f'RECEIVED_TEXT: {received_text}')

    # Execute translation function
    translated_text = aws_functions.translate_to_english(received_text)
    logger.info(f'TRANSLATED_TEXT: {translated_text}')

    # Reply message
    line_bot_api.reply_message(
        reply_token = event.reply_token,
        messages    = TextSendMessage(text=translated_text)
    )

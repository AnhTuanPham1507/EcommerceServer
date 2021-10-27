import ast

import urllib3
import json

from .config import configmomo, create_signature
from .models import Order, Payment, Seller, Revenue


def pay_momo(self, body):

    endPoint = "https://test-payment.momo.vn/v2/gateway/api/create"

    rawSignature = "accessKey=" + configmomo['accessKey'] + "&amount="+body['amount'] + \
                   "&extraData=" + body['seller_id'] + "&ipnUrl=" + configmomo['ipnUrl'] + \
                   "&orderId=" + body['order_id'] + "&orderInfo=" + "pay with momo" + \
                   "&partnerCode=" + configmomo['partnerCode'] + "&redirectUrl=" + configmomo['redirectUrl'] + \
                   "&requestId=" + body['order_id'] + "&requestType=" + 'captureWallet'

    signature = create_signature(rawSignature)

    data = {
        'partnerCode': configmomo['partnerCode'],
        'requestId': body['order_id'],
        'amount': body['amount'],
        'orderId': body['order_id'],
        'orderInfo': 'pay with momo',
        'redirectUrl': configmomo['redirectUrl'],
        'ipnUrl': configmomo['ipnUrl'],
        'lang': 'vi',
        'extraData': body['seller_id'],
        'requestType': 'captureWallet',
        'signature': signature
    }

    data = json.dumps(data)

    clen = len(data)
    http = urllib3.PoolManager()
    req = http.request(
        'POST',
        endPoint,
        headers = {
            'Content-Type' : 'application/json',
            'Content-Length' : clen
        },
        body = data
    )

    try:
        data = ast.literal_eval(req.data.decode('utf-8'))
        return {"code": req.status , "data": data}
    except Exception as e:
        return {"code": 500 , "data": e.__class__}

def signature_by_status(is_successed,body):
    if is_successed:
        res_rawSignature = "accessKey=" + configmomo['accessKey'] + "&extraData=" + '' + \
                           "&message=" + body['message'] + "&orderId=" + body['orderId'] + \
                           "&partnerCode=" + configmomo['partnerCode'] + "&requestId=" + body['requestId'] + \
                           "&responseTime=" + str(body['responseTime']) + "&resultCode=" + str(body['resultCode'])

        res_signature = create_signature(res_rawSignature)
        return {
            'partnerCode': configmomo['partnerCode'],
            'requestId': body['requestId'],
            'orderId': body['orderId'],
            'resultCode': body['resultCode'],
            'message': body['message'],
            'responseTime': body['responseTime'],
            'extraData': '',
            'signature': res_signature
        }

    else:
        res_rawSignature = "accessKey=" + configmomo['accessKey'] + "&extraData=" + '' + \
                           "&message=" + "giao dịch bị lỗi, xin vui lòng giao dịch lại" + "&orderId=" + body['orderId'] + \
                           "&partnerCode=" + configmomo['partnerCode'] + "&requestId=" + body['requestId'] + \
                           "&responseTime=" + str(body['responseTime']) + "&resultCode=" + '1003'

        res_signature = create_signature(res_rawSignature)
        return {
            'partnerCode': configmomo['partnerCode'],
            'requestId': body['requestId'],
            'orderId': body['orderId'],
            'resultCode': 1003,
            'message': 'giao dịch bị lỗi, xin vui lòng giao dịch lại',
            'responseTime': body['responseTime'],
            'extraData': '',
            'signature': res_signature
        }


def notify_momo(self, body):
    rawSignature =  "accessKey=" + configmomo['accessKey'] + "&amount=" + str(body['amount']) + \
                    "&extraData=" + body['extraData'] + "&message=" + body['message'] + \
                    "&orderId=" + body['orderId'] + "&orderInfo=" + body['orderInfo'] + \
                    "&orderType=" + body['orderType'] + "&partnerCode=" + configmomo['partnerCode'] + \
                    "&payType=" + body['payType'] + "&requestId=" + body['requestId'] + \
                    "&responseTime=" + str(body['responseTime']) + "&resultCode=" + str(body['resultCode']) + \
                    "&transId=" + str(body['transId'])

    signature = create_signature(rawSignature)

    if signature == body['signature'] and body['resultCode'] == 0:
            try:
                order = Order.objects.get(pk = int(body['orderId']))
                order.status = 2

                payment = Payment.objects.create(order = order , momo_id = body['transId'],
                                                 status = 1, type = 'MOMO')

                seller_income  = body['amount'] * 0.3
                seller = Seller.objects.get(pk = int(body['extraData']))
                seller.wallet += seller_income

                ecommerce_income = body['amount'] - seller_income
                revenue  = Revenue.objects.create(order = order, seller_income = seller_income,
                                                 ecommerce_income = ecommerce_income)

                order.save()
                payment.save()
                seller.save()
                revenue.save()
                return signature_by_status(True,body)
            except:
                return signature_by_status(False,body)
    else:
        return signature_by_status(False,body)

def check_payment(self, body):
    endPoint = "https://test-payment.momo.vn/v2/gateway/api/query"
    rawSignature = "accessKey=" + configmomo['accessKey'] + "&orderId=" + str(body['orderId']) +\
                   "&partnerCode=" + configmomo['partnerCode'] + "&requestId=" + str(body['requestId'])

    signature = create_signature(rawSignature)

    data = {
        'partnerCode': configmomo['partnerCode'],
        'requestId': body['orderId'],
        'orderId': body['orderId'],
        'lang': 'vi',
        'signature': signature
    }

    data = json.dumps(data)

    clen = len(data)
    http = urllib3.PoolManager()
    req = http.request(
        'POST',
        endPoint,
        headers={
            'Content-Type': 'application/json',
            'Content-Length': clen
        },
        body=data
    )

    try:
        data = ast.literal_eval(req.data.decode('utf-8'))
        print(data)
        if data['resultCode'] == 0 or data['resultCode'] == 9000:
                return {"code": 200 , "data": data}
        else:
            return {"code": 400 , "data": data}
    except Exception as e:
        return {"code": 500 , "data": e.__class__}









import hashlib
import hmac

configmomo = dict(
    partnerCode= "MOMOUR2S20210830",
    accessKey= "zV8bQQqebfkOpXm8",
    serectKey= "URjMechix19xzhkqAP7Ev1Zhqyo5ZWEt",
    redirectUrl= 'https://ecommerceapp1507.herokuapp.com/order/',
    ipnUrl= "https://ecommerce1507server.herokuapp.com/notifymomo/",
)

def create_signature(rawSignature):

  key_byte = bytes(configmomo['serectKey'], 'utf-8')
  data_byte = bytes(rawSignature, 'utf-8')

  h = hmac.new(key_byte, data_byte, hashlib.sha256)
  return h.hexdigest()

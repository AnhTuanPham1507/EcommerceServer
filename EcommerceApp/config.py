import hashlib
import hmac

configmomo = dict(
    partnerCode= "MOMOUR2S20210830",
    accessKey= "zV8bQQqebfkOpXm8",
    serectKey= "URjMechix19xzhkqAP7Ev1Zhqyo5ZWEt",
    redirectUrl= 'http://nervous-cougar-61.loca.lt/order/',
    ipnUrl= "http://5b77-27-3-240-77.ngrok.io/notifymomo/",
)

def create_signature(rawSignature):

  key_byte = bytes(configmomo['serectKey'], 'utf-8')
  data_byte = bytes(rawSignature, 'utf-8')

  h = hmac.new(key_byte, data_byte, hashlib.sha256)
  return h.hexdigest()
import base64
import hashlib
import hmac
import json
import os
import random
import time
from urllib import request

'''
调用腾讯实时语音识别 API
'''

signBase = 'POSTasr.cloud.tencent.com/asr/v1/'
# 各参数根据需要进行调整
appid = ''
secretid = ''
secret_key = ''
projectid = 0
sub_service_type = 1
engine_model_type = '16k_0'
result_text_format = 0
res_type = 0
voice_format = 1
timestamp = ''
expired = ''
needvad = 0
nonce = ''
seq = ''
end = ''
source = 0
voice_id = ''
timeout = 5000
cutLength = 20000
# 录音文件路径
input_filename = 'input.wav'
input_filepath = os.getcwd() + '/wav/'
filepath = input_filepath + input_filename


# 生成随机 nonce
def randNonce():
    ran = random.randint(1000, 9999)
    print('nonce:' + str(ran))
    return ran


# 生成随机 voice_id
def randVoiceId(n):
    seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    temp = []
    for i in range(n):
        temp.append(random.choice(seed))
    str = ''.join(temp)
    print('voice_id:' + str)
    return str


# 生成签名原文
def formatSignString(appid, params):
    url = signBase + appid + '?'
    for k, v in params.items():
        url += k
        url += '='
        url += str(v)
        url += '&'
    url = url[:-1]
    print('url:' + url)
    return url


# 生成签名串
def sign(url, secret_key):
    bytes_url = bytes(url, 'utf-8')
    bytes_secret_key = bytes(secret_key, 'utf-8')
    hmacStr = hmac.new(bytes_secret_key, bytes_url, hashlib.sha1).digest()
    s = base64.b64encode(hmacStr)
    print('sign:' + str(s))
    return s


# 发送 http 请求
def sendHttp(appid, secretid, secret_key, projectid, sub_service_type, engine_model_type, result_text_format, res_type,
             voice_format, needvad, source, timeout, filepath, cutLength):
    params_arr = dict()
    params_arr['projectid'] = projectid
    params_arr['secretid'] = secretid
    params_arr['sub_service_type'] = sub_service_type
    params_arr['engine_model_type'] = engine_model_type
    params_arr['result_text_format'] = result_text_format
    params_arr['res_type'] = res_type
    params_arr['voice_format'] = voice_format
    params_arr['needvad'] = needvad
    params_arr['source'] = source
    params_arr['timeout'] = timeout
    params_arr['timestamp'] = str(int(time.time()))
    params_arr['expired'] = int(time.time()) + 24 * 60 * 60
    params_arr['nonce'] = randNonce()
    params_arr['voice_id'] = randVoiceId(16)
    # 获取文件
    file_object = open(filepath, 'rb')
    file_object.seek(0, os.SEEK_END)
    datalen = file_object.tell()
    file_object.seek(0, os.SEEK_SET)
    seq = 0
    # 分片
    while (datalen > 0):
        end = 0
        if (datalen < cutLength):
            end = 1
        params_arr['seq'] = seq
        params_arr['end'] = end
        # 需要对参数进行排序后再拼接成原文
        params = dict()
        for i in sorted(params_arr):
            params[i] = params_arr[i]
        url = formatSignString(appid, params)
        # 根据原文生成签名串
        auth = sign(url, secret_key)
        # 获取文件内容
        if (datalen < cutLength):
            content = file_object.read(datalen)
        else:
            content = file_object.read(cutLength)
        seq += 1
        datalen -= cutLength
        # 设置请求头
        headers = {}
        headers['Host'] = 'asr.cloud.tencent.com'
        headers['Authorization'] = auth
        headers['Content-Type'] = 'application/octet-stream'
        headers['Content-Length'] = len(content)
        # 拼接请求 url
        requestUrl = 'http://'
        requestUrl += url[4::]

        req = request.Request(requestUrl, data=content, headers=headers)

        res_data = request.urlopen(req)
        # 获取响应 res
        res = res_data.read().decode('utf-8')
        print(res)
    # 关闭文件
    file_object.close()

    return res


# 获取响应结果
def getResult():
    res = sendHttp(appid=appid, secretid=secretid, secret_key=secret_key, projectid=projectid,
                   sub_service_type=sub_service_type, engine_model_type=engine_model_type,
                   result_text_format=result_text_format, res_type=res_type, voice_format=voice_format, needvad=needvad,
                   source=source, timeout=timeout, filepath=filepath, cutLength=cutLength)
    res_dict = json.loads(res)
    data = res_dict.get('text')
    return data


if __name__ == '__main__':
    getResult()

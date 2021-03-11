def isReplayAttack(appId, timestamp, nonce, signature):
    key = PREFIX + appId + "_" + timestampe + "_" + nonce
    obj = redisUtil.get(key)
    if (obj != NULL and signature.equals(obj)):
        return False
    else:
        redisUtil.set(key, signatuer, TIME_DIFF_MAX)
    return true

def generateSign(sortedMap, appSecret):
    sortedMap.remove(Constant.SIGN)
    plainText = Buff()
    digest = plaitex + appSecret
    return DigestUtils.md5DigestAsHex()

def verifySign(params, appSecret):
   urlSign = params.get(Constant.SIGN)


def getBodyString(request) throw Except:
    pass

def getAllParams(request) throw Except:
    appId = request.getHeader(Constant.APP_ID)
    timestamp = request.getHeader(Constant.TIME_STAMP)
    sign = request.getHeader(Constant,.SIGN)
    nonce = request.getHeader(Constant.NONCE)


def verifyHeaderParams(request):
    appId = request.getHeader(Constant.APP_ID)
    if appId.isEmpty():
        return False
    timestamp = request.getHeader(Constant.TIME_STAMP)
    if timestamp.isEmpty():
        return False
    sign = request.getHeader(Constant.SIGN)
    if sign.isEmpty():
        return False
    nonce = request.getHeader(Constant.NONCE):
    if nonce.isEmpty():
        return False
    diff = time.time() - timestamp
    if diff > 100 * * 10:
        return False
    return True


def doFilterInternal(request, response, FileterChain.filterChain) throw Except:
    pass
    return True
 

# Base64

Base64 是一种用 64 个字符来表示任意二进制数据的方法。

**编码与解码的处理对象是byte，因此编码前需要将str转为byte；解码后输出的是byte对象，需要解码成str。**

## JavaScript 实现

```javascript
// 引用 crypto-js 加密模块
const CryptoJS = require('crypto-js')

function base64Encode(text) {
    let srcs = CryptoJS.enc.Utf8.parse(text);
    let encodeData = CryptoJS.enc.Base64.stringify(srcs);
    return encodeData;
}
function base64Decode(encodeData){
    let srcs = CryptoJS.enc.Base64.parse(encodeData);
    let decodeData = srcs.toString(CryptoJS.enc.Utf8);
    return decodeData;
}

const text = 'Hello world';
let encodeData = base64Encode(text);
let decodeData = base64Decode(encodeData);
console.log('Base64编码: ', encodeData);
console.log('Bas64解码: ', decodeData);
```

## Python 实现

```python
import base64

def base64_encode(text):
    encode_data = base64.b64encode(text.encode())
    return encode_data

def base64_decode(encode_data):
    decode_data = base64.b64encode(encode_data)
    return decode_data

text = 'Hello world'
encode_data = base64_encode(text)
decode_data = base64_decode(encode_data)
print('Base64 编码：', encode_data)
print('Base64 解码：', decode_data)
```

# MD5

## JavaScript 实现

```javascript
// 引用 crypto-js 加密模块
const CryptoJS = require('crypto-js')

function MD5(text){
    return CryptoJS.MD5(text).toString();
}

console.log(MD5('Hello world'))
```

## Python 实现

```python
import hashlib

text = 'Hello world'
md5_text = hashlib.md5(text.encode()).hexdigest()
print('MD5密文：', md5_text)
```

# HMAC

## JavaScript 实现

```javascript
const CryptoJS = require('crypto-js')

function HMACEncrypt(text, key){
    return CryptoJS.HmacMD5(text, key).toString();
}

let text = 'Hello world'
let key = 'secret'
console.log(HMACEncrypt(text, key))
```

## Python 实现

```python
import hmac

def hmac_encrypt(text, key):
    text = text.encode()
    key = key.encode()
    md5 = hmac.new(key, text, digestmod='MD5')
    return md5.hexdigest()

text = 'hello world'
key = 'a_encode_key'
print(hmac_encrypt(text, key))
```

# AES

## JavaScript 实现

```javascript
const CryptoJS = require('crypto-js');

function AesEncrypt(aesKey, aesIv, text) {
    let key = CryptoJS.enc.Utf8.parse(aesKey),
        iv = CryptoJS.enc.Utf8.parse(aesIv),
        srcs = CryptoJS.enc.Utf8.parse(text),
        // CBC加密方式, Pkcs7填充方式
        encrypted = CryptoJS.AES.encrypt(srcs, key, {
            iv: iv,
            mode: CryptoJS.mode.CBC,
            padding: CryptoJS.pad.Pkcs7
        });
    return encrypted.toString();
}

function AesDecrypt(aesKey, aesIv, encryptedData){
    let key = Crypto.enc.Utf8.parse(aesKey),
        iv = CryptoJS.enc.Utf8.parse(aesIv),
        srcs = encryptedData,
        decrypted = CryptoJS.AES.decrypt(srcs, key, {
            iv: iv,
            mode: CryptoJS.mode.CBC,
            padding: CryptoJS.pad.Pkcs7
        });
    return decrypted.toString(CryptoJS.enc.Utf8)
}

const text = "Hello world!"       // 待加密对象
const aesKey = "6f726c64f2c2057c"   // 密钥，16 倍数
const aesIv = "0123456789ABCDEF"    // 偏移量，16 倍数

const encryptedData = AesEncrypt()
const decryptedData = AesDecrypt()

console.log("加密字符串: ", encryptedData)
console.log("解密字符串: ", decryptedData)

```

## Python 实现

```python
import base64
from Crypto.Cipher import AES

# 补位函数
def pad_to_16(value):
    while len(value) % 16 != 0:
        value += '\0'
    return str.encode(value)

# 加密
def aes_encrypt(key, text, iv):
    # 初始化加密器
    aes = AES.new(pad_to_16(key), AES.MODE_CBC, pad_to_16(iv))
    encrypt_aes = aes.encrypt(pad_to_16(text))
    encrypt_text = str(base64.encodebytes(encrypt_aes), encoding='utf-8')
    return encrypt_text

# 解密
def aes_decrypt(key, encrypt_text, iv):
    aes = AES.new(pad_to_16(key), AES.MODE_CBC, pad_to_16(iv))
    base64_decrypted = base64.decodebytes(encrypt_text.encode(encoding='utf-8'))
    decrypt_text = str(aes.decrypt(base64_decrypted), encoding='utf-8').replace('\0', '')
    return decrypt_text
```

# RSA

## JavaScript 实现

```javascript
const NodeRSA = require('node-rsa');

function rsaEncrypt() {
    let pubKey = new NodeRSA(publicKey,'pkcs8-public');
    let encryptedData = pubKey.encrypt(text, 'base64');
    return encryptedData
}

function rsaDecrypt() {
    let priKey = new NodeRSA(privatekey,'pkcs8-private');
    let decryptedData = priKey.decrypt(encryptedData, 'utf8');
    return decryptedData
}

var key = new NodeRSA({b: 512});                    //生成512位秘钥
var publicKey = key.exportKey('pkcs8-public');    //导出公钥
var privatekey = key.exportKey('pkcs8-private');  //导出私钥
var text = "I love Python!"

var encryptedData = rsaEncrypt()
var decryptedData = rsaDecrypt()

console.log("公钥:\n", publicKey)
console.log("私钥:\n", privatekey)
console.log("加密字符串: ", encryptedData)
console.log("解密字符串: ", decryptedData)
```

## Python 实现

```python
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5


data = "cKK8B2rWwfwWeXhz"
public_key = "MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAM1xhOWaThSMpfxFsjV5YaWOFHt+6RvS+zH2Pa47VVr8PkZYnRaaKKy2MYBuEh7mZfM/R1dUXTgu0gp6VTNeNQkCAwEAAQ=="
rsa_key = RSA.import_key(base64.b64decode(public_key))  # 导入读取到的公钥
cipher = PKCS1_v1_5.new(rsa_key)                        # 生成对象
cipher_text = base64.b64encode(cipher.encrypt(data.encode(encoding="utf-8")))
print(cipher_text)


# RSA模块实现
import rsa


def rsa_encrypt(pu_key, t):
    # 公钥加密
    rsa = rsa.encrypt(t.encode("utf-8"), pu_key)
    return rsa


def rsa_decrypt(pr_key, t):
    # 私钥解密
    rsa = rsa.decrypt(t, pr_key).decode("utf-8")
    return rsa


if __name__ == "__main__":
    public_key, private_key = rsa.newkeys(512)   # 生成公钥、私钥
    print('公钥：', public_key)
    print('私钥：', private_key)
    text = 'I love Python!'  # 加密对象
    encrypted_str = rsa_encrypt(public_key, text)
    print('加密字符串：', encrypted_str)
    decrypted_str = rsa_decrypt(private_key, encrypted_str)
    print('解密字符串：', decrypted_str)
```


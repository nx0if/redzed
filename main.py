import asyncio
import aiohttp
from flask import Flask, request, jsonify
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import binascii
from secret import*
import uid_generator_pb2

app = Flask(__name__)

# Helper function to create protobuf message
def create_protobuf(saturn_, garena):
    message = uid_generator_pb2.uid_generator()
    message.saturn_ = saturn_
    message.garena = garena
    return message.SerializeToString()

# Convert protobuf data to hex
def protobuf_to_hex(protobuf_data):
    return binascii.hexlify(protobuf_data).decode()

# Encrypt data using AES encryption
def encrypt_aes(hex_data, key, iv):
    key = key.encode()[:16]
    iv = iv.encode()[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_data = pad(bytes.fromhex(hex_data), AES.block_size)
    encrypted_data = cipher.encrypt(padded_data)
    return binascii.hexlify(encrypted_data).decode()

# Perform the like request
async def like(id, session, token):
    like_url = 'https://clientbp.ggblueshark.com/LikeProfile'
    headers = {
        'X-Unity-Version': '2018.4.11f1',
        'ReleaseVersion': 'OB46',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-GA': 'v1 1',
        'Authorization': f'Bearer {token}',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.1.2; ASUS_Z01QD Build/QKQ1.190825.002)',
        'Host': 'clientbp.ggblueshark.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip'
    }

    data = bytes.fromhex(id)

    async with session.post(like_url, headers=headers, data=data) as response:
        status_code = response.status
        response_text = await response.text()
        return {'status_code': status_code, 'response_text': response_text}

# Fetch tokens from external service
async def get_tokens(session):
    url = 'https://get-token-f5-3h5h.onrender.com/token'
    async with session.get(url) as response:
        tokens = await response.json()
        return [token['token'] for token in tokens]

# Async function to send like requests
async def sendlike(uid):
    saturn_ = int(uid)
    garena = 1
    protobuf_data = create_protobuf(saturn_, garena)
    hex_data = protobuf_to_hex(protobuf_data)
    aes_key = key
    aes_iv = iv
    id = encrypt_aes(hex_data, aes_key, aes_iv)

    async with aiohttp.ClientSession() as session:
        tokens = await get_tokens(session)
        tasks = [like(id, session, token) for token in tokens[:500]]
        results = await asyncio.gather(*tasks)
    return results

# Flask route to handle GET requests with UID as a query parameter
@app.route('/like', methods=['GET'])
def like_endpoint():
    try:
        uid = request.args.get('uid')  # Extract UID from URL query parameters
        if not uid:
            return jsonify({'error': 'Missing uid parameter'}), 400
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        results = loop.run_until_complete(sendlike(uid))
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

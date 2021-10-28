from sanic import Sanic, request, response
import aiofiles
import secrets
import os
import functools


app = Sanic('TennisCdn')


def getsize():
    size = 0
    for x in os.scandir('./cdn_items/'):
        size + =os.path.getsize(x)
    return size

async def get_size():
    thing = functools.partial(getsize)
    return await app.loop.run_in_executor(None, thing)

@app.route('/<path>', methods=['GET'])
async def cdn_serve(request: request, path):
    return await response.file_stream(f'./cdn_items/{path}', status=200)

@app.route('/upload', methods=['POST'])
async def cdn_upload(request):
    name, extension = os.path.splitext(request.files['file'][0].name)
    path = secrets.token_urlsafe(30) + extension
    async with aiofiles.open(f'./cdn_items/{path}', 'wb') as f:
        try:
            await f.write(request.files['file'][0].body)
        except Exception:
            return response.json({'status': 'failed'}, status=500)
        else:
            return response.json({'status': 'success', 'location': f'https://cdn.tennisbowling.com/{path}'})

@app.route('/list', methods=['GET'])
async def cdn_list(request):
    return response.json({'items': os.listdir('./cdn_items/')})

@app.route('/size', methods=['GET'])
async def cdn_size(request):
    return response.json({'size': (await get_size())})
        
       
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081, workers=4)

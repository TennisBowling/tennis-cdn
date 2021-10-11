from sanic import Sanic, request, response
import aiofiles
import secrets
import os


app = Sanic('TennisCdn')

@app.route('/<path>', methods=['GET'])
async def cdn_serve(request: request, path):
    return await response.file_stream(f'.pyt/cdn_items/{path}', status=200)

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)

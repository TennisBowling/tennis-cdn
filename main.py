from sanic import Sanic, request, response
import aiofiles
import secrets


app = Sanic('TennisCdn')

@app.route('/<path>', methods=['GET'])
async def cdn_serve(request: request, path):
    return await response.file_stream(f'../cdn_items/{path}', status=200)

@app.route('/upload', methods=['POST'])
async def cdn_upload(request):
    path = str(secrets.randbelow(5000000000000000000000)) + request.files["file"][0].name
    async with aiofiles.open(f'./cdn_items/{path}', 'wb') as f:
        try:
            await f.write(request.files['file'][0].body)
        except Exception:
            return response.json({'status': 'failed'})
        else:
            return response.json({'status': 'success', 'location': f'http://localhost:8080/{path}'})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
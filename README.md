# tennis-cdn
This is the source code for [my cdn](https://cdn.tennisbowling.com).  
You can run this if you want to, but if you want to use my cdn directly, make a POST request to https://cdn.tennisbowling.com/upload with a file attached.  
Requests example:  
send file  
```python
import requests

 f = open('a.txt') # replace this with your file
 r = requests.post('https://cdn.tennisbowling.com/upload', files={'file': f}) # if this throws something with ssl error set a `secure=False` kwarg.
 print(r.json()) # get the location of the file uploaded.
 ```
 get file  
 ```python
 import requests
 r = requests.get('https://cdn.tennisbowling.com/filelocation')
 print(r.text)
 ```

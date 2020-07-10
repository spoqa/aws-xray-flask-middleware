# spoqa-aws-xray-flask-middleware

Spoqa flavoured AWS X-Ray middleware for Flask

**Before**:

```
https://example.com/api/12345/messages
http://localhost:8000/api/32123/messages
http://127.0.0.1/api/43434/messages
...
```

**After**:

```
//service_name/api/<int:id>/messages
```

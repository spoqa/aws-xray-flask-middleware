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

## Usage

Replace `aws_xray_sdk.ext.flask.middleware.XRayMiddleware` with `spoqa_aws_xray_flask_middleware.XRayMiddleware`

```python
from aws_xray_sdk.core import xray_recorder
from spoqa_aws_xray_flask_middleware import XRayMiddleware

app = Flask(__name__)

xray_recorder.configure(service='fallback_name', dynamic_naming='*mysite.com*')
XRayMiddleware(app, xray_recorder)
```

import os
from fastserve.models import FaceDetection

#example of getting environment variables setted in docker-compose.yml
batch_size = os.environ.get('BATCH_SIZE', 2)
timeout = os.environ.get('TIMEOUT', 1)


app = FaceDetection(batch_size=batch_size, timeout=timeout)
app.run_server(host='0.0.0.0')



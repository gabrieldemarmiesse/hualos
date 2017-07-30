from keras.callbacks import Callback
import json
try:
    import requests
except ImportError:
    requests = None

class RemoteMonitor(Callback):
    """Callback used to stream events to a server.

    Requires the `requests` library.
    Events are sent to `root + '/publish/epoch/end/'` by default. Calls are
    HTTP POST, with a `data` argument which is a
    JSON-encoded dictionary of event data.

    # Arguments
        root: String; root url of the target server.
        path: String; path relative to `root` to which the events will be sent.
        field: String; JSON field under which the data will be stored.
        headers: Dictionary; optional custom HTTP headers.
            Defaults to:
            `{'Accept': 'application/json',
              'Content-Type': 'application/json'}`
    """

    def __init__(self,
                 root='http://localhost:9000',
                 path='/publish/epoch/end/',
                 field='data'):
        super(RemoteMonitor, self).__init__()
        self.root = root
        self.path = path
        self.field = field

    def on_epoch_end(self, epoch, logs=None):
        if requests is None:
            raise ImportError('RemoteMonitor requires '
                              'the `requests` library.')
        logs = logs or {}
        send = {}
        send['epoch'] = epoch
        for k, v in logs.items():
            send[k] = v
        try:
            requests.post(self.root + self.path,
                          {self.field: json.dumps(send)})
        except requests.exceptions.RequestException:
            warnings.warn('Warning: could not reach RemoteMonitor '
                          'root server at ' + str(self.root))
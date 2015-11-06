# Python Google App Engine Example

Get started quickly with Pusher and Python on Google App Engine. 

Add to your `requirements.txt`:

```
pusher
```

Then vendor the `pusher` package to a folder - e.g. `lib/` with:

    $ pip2.7 install -t lib -r requirements.txt

When initializing Pusher in your Python code, make sure to import the library's `GAEBackend`, which is used to send requests to our HTTP API using Google's [urlfetch](https://cloud.google.com/appengine/docs/python/urlfetch) service.

```python
p = pusher.Pusher(
  app_id=app_id,
  key=key,
  secret=secret,
  backend=pusher.gae.GAEBackend # tell the library to use urlfetch for requests
)

p.trigger('test_channel', 'my_event', {'hello': 'world'})
```
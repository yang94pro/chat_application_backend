import redis
from celery import Celery

r = redis.Redis(host="redis-18476.c124.us-central1-1.gce.cloud.redislabs.com",port="18476", password="H4bNIEJ1ZA477jeRNMEIuVxmIjCGVjun")
app = Celery('task', broker=r)

@app.task
def add(x,y):
    return x+y
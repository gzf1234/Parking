
import redis
conn = redis.Redis(host='118.25.42.92', port=6379, db=0)
a = '上海浦东*'
b = conn.keys(a.encode('utf-8'))

# conn.bgsave()
print(b)

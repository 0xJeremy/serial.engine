from serialengine.connection import connection
import time

conn = connection("/dev/ttyACM0", baud=2000000, timeout=1).start()

while not conn.opened:
    pass

conn.write("test", "hello there")

while conn.get("test") == None:
    pass

print("SUCCESS:", conn.get("test"))

conn.close()

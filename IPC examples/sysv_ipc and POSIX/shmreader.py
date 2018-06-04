import sysv_ipc
import time

# Create shared memory object
memory = sysv_ipc.SharedMemory(123456, sysv_ipc.IPC_CREX, 0)

memory.write(bytes("hello", "ascii"))

# Read value from shared memory
memory_value = memory.read()

# Find the 'end' of the string and strip
i = memory_value.find(b'\0')
if i != -1:
    memory_value = memory_value[:i]

print(memory_value.decode("ascii").strip())

while memory_value.decode("ascii").strip() == "hello":
    time.sleep(10)    

memory.detach()

memory.remove()
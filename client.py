import time, sys, random
from threading import Thread, Event
import requests

def main(thread_count):
    threads = []
    event = Event()
    event.set()

    for id in range(thread_count):
        thread = Thread(target=send, args = (id, event), daemon=True)
        thread.start()
        threads.append(thread)

    try:
        while True:
            time.sleep(.01)
    except KeyboardInterrupt:
        # Stop All threads on Ctrl-C event from keyboard
        print("Stoping all threads")
        event.clear()
        for thread in threads:
            thread.join()


def send(id, event):
    count = 0
    while event.is_set():
        wait_time_ms = random.randint(0, 1000)
        print("ClientId={} waiting {}ms, count={}".format(id, wait_time_ms, count))
        r = requests.get("http://127.0.0.1:5000/?clientId={}".format(id))
        if r.status_code != 200:
            print("ClientId={} - Request count={} rejected".format(id, count))
        time.sleep(wait_time_ms / 1000)
        count += 1


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Missing numbers of threads to start Client")
        sys.exit(1)
    thread_count = int(sys.argv[1])

    if thread_count <= 0:
        print("Number of threads must be greater than 0")
        sys.exit(1)

    print("Starting execution...  [press Ctrl+C to stop]")
    time.sleep(3)
    main(thread_count)
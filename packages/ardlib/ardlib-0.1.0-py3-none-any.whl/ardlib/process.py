import os
import time
import threading
import multiprocessing
from typing import Any, Callable, List

spawned_child: List[Any] = []

spawned_process: List[multiprocessing.Process] = []
spawned_process_daemon: List[multiprocessing.Process] = []

spawned_thread: List[threading.Thread] = []
spawned_thread_daemon: List[threading.Thread] = []

def spawn_child():
    pid = os.fork()
    spawned_child.append(pid)
    if pid != 0:
        os.waitpid(pid, 0)

def spawn_process(function: Callable[[], Any]):
    process = multiprocessing.Process(target=function, daemon=True)
    spawned_process.append(process)
    process.start()

def spawn_process_daemon(function: Callable[[], Any]):
    process_daemon = multiprocessing.Process(target=function, daemon=True)
    spawned_process_daemon.append(process_daemon)
    process_daemon.start()


def spawn_thread(function: Callable[[], Any]):
    thread = threading.Thread(target=function, daemon=False)
    spawned_thread.append(thread)
    thread.start()

def spawn_thread_daemon(function: Callable[[], Any]):
    thread_daemon = threading.Thread(target=function, daemon=True)
    spawned_thread_daemon.append(thread_daemon)
    thread_daemon.start()

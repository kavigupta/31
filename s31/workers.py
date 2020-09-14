import tempfile
import uuid
import time

from .utils import get_keys


def dispatch_workers(num_workers, launch_worker, arguments):
    used_workers = [None] * num_workers
    arguments = arguments[::-1]  # so we can pop from the back
    completed = 0
    file = tempfile.mktemp()
    while True:
        # check if any workers have completed
        dones = get_keys(file)
        for i, x in enumerate(used_workers):
            if x in dones:
                completed += 1
                used_workers[i] = None

        free = [i for i, w in enumerate(used_workers) if w is None]

        if len(free) == num_workers and not arguments:
            print("All tasks completed")
            return

        print(
            "Completed: {}, In Progress: {}, Queued: {}".format(
                completed, num_workers - len(free), len(arguments)
            )
        )

        if not free or not arguments:
            # Wait for some process to become free, or just wait for everything to end
            time.sleep(1)
            continue

        worker_idx = free[0]
        used_workers[worker_idx] = str(uuid.uuid4())
        launch_worker(worker_idx, arguments.pop(), file, used_workers[worker_idx])

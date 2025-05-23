from task_runner import TaskRunner
import os

os.chdir("..")

if __name__ == '__main__':
    tag = "bsdr_salinas2"
    tasks = {
        "algorithms" : ["bsdr"],
        "datasets": [
            "salinas"
        ],
        "target_sizes" : [5]
    }

    ev = TaskRunner(tasks,tag,skip_all_bands=True, verbose=True)
    summary, details = ev.evaluate()

from task_runner import TaskRunner
import os

os.chdir("..")

if __name__ == '__main__':
    tag = "bsdr_ip"
    tasks = {
        "algorithms" : ["bsdr"],
        "datasets": [
            "indian_pines"
        ],
        "target_sizes" : [8]
    }
    ev = TaskRunner(tasks,tag,skip_all_bands=True, verbose=True)
    summary, details = ev.evaluate()

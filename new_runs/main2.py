from task_runner import TaskRunner
import os

os.chdir("..")

if __name__ == '__main__':
    tag = "v9_weight"
    tasks = {
        "algorithms" : ["v9_weight"],
        "datasets": [
            "indian_pines"
        ],
        "target_sizes" : [30]
    }
    ev = TaskRunner(tasks,tag,skip_all_bands=True, verbose=True)
    summary, details = ev.evaluate()

from task_runner import TaskRunner
import os

os.chdir("..")

if __name__ == '__main__':
    tag = "v9_grad"
    tasks = {
        "algorithms" : ["v9_grad"],
        "datasets": [
            "ghisaconus"
        ],
        "target_sizes" : [30]
    }
    ev = TaskRunner(tasks,tag,skip_all_bands=True, verbose=False)
    summary, details = ev.evaluate()

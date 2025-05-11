from task_runner import TaskRunner
import os

os.chdir("..")

if __name__ == '__main__':
    tag = "bsdr_gh3"
    tasks = {
        "algorithms" : ["bsdr"],
        "datasets": [
            "ghisaconus"
        ],
        "target_sizes" : [20]
    }

    ev = TaskRunner(tasks,tag,skip_all_bands=True, verbose=True)
    summary, details = ev.evaluate()

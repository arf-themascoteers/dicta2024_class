from task_runner import TaskRunner
import os

os.chdir("..")

if __name__ == '__main__':
    tag = "all_bands"
    tasks = {
        "algorithms" : ["pcal"],
        "datasets": [
            "indian_pines",
            "paviaU",
            "salinas",
            "ghisaconus"
        ],
        "target_sizes" : [8]
    }
    ev = TaskRunner(tasks,tag,skip_all_bands=False, verbose=False)
    summary, details = ev.evaluate()

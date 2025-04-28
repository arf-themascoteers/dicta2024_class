from task_runner import TaskRunner
import os

os.chdir("..")

if __name__ == '__main__':
    tag = "v0"
    tasks = {
        "algorithms" : ["v0"],
        "datasets": ["ghisaconus"],
        "target_sizes" : list(range(30,4,-1))
    }
    ev = TaskRunner(tasks,tag,skip_all_bands=False, verbose=True)
    summary, details = ev.evaluate()

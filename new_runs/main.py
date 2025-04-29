from task_runner import TaskRunner
import os

os.chdir("..")

if __name__ == '__main__':
    tag = "spa_all"
    tasks = {
        "algorithms" : ["spa"],
        "datasets": [
            "ghisaconus","indian_pines","paviaU","salinas"
        ],
        "target_sizes" : list(range(30,4,-1))
    }
    ev = TaskRunner(tasks,tag,skip_all_bands=True, verbose=False)
    summary, details = ev.evaluate()

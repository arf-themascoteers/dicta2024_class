import train_test_evaluator


def report_stats(model, epoch, mse_loss):
    if not model.verbose:
        return

    selected_bands = model.get_indices()
    r2, rmse, rpd = train_test_evaluator.evaluate_dataset(model.dataset, model)
    model.reporter.report_bsdr_epoch(epoch, mse_loss,r2,rmse,rpd,selected_bands)

    PRINT = True
    if PRINT:
        m = [epoch, mse_loss,r2,rmse,rpd,selected_bands]
        if epoch == 0:
            names = ['epoch', 'mse_loss','oa','aa','k','selected_bands']
            print(''.join(name.ljust(10) for name in names))
        m = [x.item() if hasattr(x, 'item') else x for x in m]
        m = [round(x, 3) if isinstance(x, float) else x for x in m]
        print(''.join(str(v).ljust(10) for v in m))


def get_number_of_classes(name):
    class_counts = {
        "indian_pines": 16,
        "paviaU": 10,
        "salinas": 16,
        "ghisaconus": 5
     }
    return class_counts[name]
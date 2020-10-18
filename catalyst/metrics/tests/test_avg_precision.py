import numpy as np

import torch

from catalyst import metrics


def test_map():
    """
    Tets for catalyst.metrics.map metric.
    """

    # check everything is relevant
    y_pred = [0.5, 0.2, 0.3, 0.8]
    y_true = [1.0, 1.0, 1.0, 1.0]

    average_precision = metrics.avg_precision(
        torch.Tensor([y_pred]), torch.Tensor([y_true])
    )
    assert average_precision[0] == 1

    # check is everything is relevant for 3 users
    y_pred = [0.5, 0.2, 0.3, 0.8]
    y_true = [1.0, 1.0, 1.0, 1.0]

    average_precision = metrics.avg_precision(
        torch.Tensor([y_pred, y_pred, y_pred]),
        torch.Tensor([y_true, y_true, y_true]),
    )
    assert average_precision[0] == torch.ones(3, len(y_true))

    # check everything is irrelevant
    y_pred = [0.5, 0.2, 0.3, 0.8]
    y_true = [1.0, 1.0, 1.0, 1.0]

    average_precision = metrics.avg_precision(
        torch.Tensor([y_pred]), torch.Tensor([y_true])
    )
    assert average_precision[0] == 0

    # check is everything is irrelevant for 3 users
    y_pred = [0.5, 0.2, 0.3, 0.8]
    y_true = [1.0, 1.0, 1.0, 1.0]

    average_precision = metrics.avg_precision(
        torch.Tensor([y_pred, y_pred, y_pred]),
        torch.Tensor([y_true, y_true, y_true]),
    )
    assert average_precision[0] == torch.zeros(3, len(y_true))

    # check 4 test with k
    y_pred1 = [4.0, 2.0, 3.0, 1.0]
    y_pred2 = [1.0, 2.0, 3.0, 4.0]
    y_true1 = [0.0, 1.0, 1.0, 1.0]
    y_true2 = [0.0, 1.0, 0.0, 0.0]

    y_pred_torch = torch.Tensor([y_pred1, y_pred2])
    y_true_torch = torch.Tensor([y_true1, y_true2])

    average_precision = metrics.avg_precision(y_pred_torch, y_true_torch, k=3)
    assert np.around(average_precision[0]) == 0.39
    assert np.around(average_precision[1]) == 0.11

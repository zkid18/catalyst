import numpy as np

import torch

from catalyst import metrics


def test_avg_precision():
    """
    Tests for catalyst.metrics.avg_precision metric.
    """
    # # check everything is relevant
    y_pred = [0.5, 0.2, 0.3, 0.8]
    y_true = [1.0, 1.0, 1.0, 1.0]

    average_precision = metrics.avg_precision(
        torch.Tensor([y_pred]), torch.Tensor([y_true])
    )
    assert average_precision[0] == 1

    # # check is everything is relevant for 3 users
    y_pred = [0.5, 0.2, 0.3, 0.8]
    y_true = [1.0, 1.0, 1.0, 1.0]

    average_precision = metrics.avg_precision(
        torch.Tensor([y_pred, y_pred, y_pred]),
        torch.Tensor([y_true, y_true, y_true]),
    )
    assert torch.equal(average_precision, torch.ones(3))

    # # check everything is irrelevant
    y_pred = [0.5, 0.2, 0.3, 0.8]
    y_true = [0.0, 0.0, 0.0, 0.0]

    average_precision = metrics.avg_precision(
        torch.Tensor([y_pred]), torch.Tensor([y_true])
    )
    assert average_precision[0] == 0

    # # check is everything is irrelevant for 3 users
    y_pred = [0.5, 0.2, 0.3, 0.8]
    y_true = [0.0, 0.0, 0.0, 0.0]

    average_precision = metrics.avg_precision(
        torch.Tensor([y_pred, y_pred, y_pred]),
        torch.Tensor([y_true, y_true, y_true]),
    )
    assert torch.equal(average_precision, torch.zeros(3))

    # # check 4 test with k
    y_pred1 = [4.0, 2.0, 3.0, 1.0]
    y_pred2 = [1.0, 2.0, 3.0, 4.0]
    y_true1 = [0.0, 1.0, 1.0, 1.0]
    y_true2 = [0.0, 1.0, 0.0, 0.0]

    y_pred_torch = torch.Tensor([y_pred1, y_pred2])
    y_true_torch = torch.Tensor([y_true1, y_true2])

    average_precision = metrics.avg_precision(y_pred_torch, y_true_torch, k=3)

    assert np.isclose(average_precision[0], 0.5833, atol=1e03)
    assert np.isclose(average_precision[1], 0.333, atol=1e03)

    # check 5
    # Stanford Introdcution to information retrieval primer
    y_pred1 = np.arange(9, -1, -1)
    y_true1 = [1.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0]
    y_pred2 = np.arange(9, -1, -1)
    y_true2 = [0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0]

    y_pred_torch = torch.Tensor([y_pred1, y_pred2])
    y_true_torch = torch.Tensor([y_true1, y_true2])

    average_precision = metrics.avg_precision(y_pred_torch, y_true_torch)

    assert np.allclose(
        [average_precision[0], 0.6222], [average_precision[1], 0.4429], atol=1e03
    )


def test_mean_avg_precision():
    """
    Tests for catalyst.metrics.mean_avg_precision metric.
    """
    # check 1
    # Stanford Introdcution to information retrieval primer
    y_pred1 = np.arange(9, -1, -1)
    y_true1 = [1.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0]
    y_pred2 = np.arange(9, -1, -1)
    y_true2 = [0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0]

    y_pred_torch = torch.Tensor([y_pred1, y_pred2])
    y_true_torch = torch.Tensor([y_true1, y_true2])

    top_k = [10]
    map_at10 = metrics.mean_avg_precision(y_pred_torch, y_true_torch, top_k)[0]

    assert np.allclose(map_at10, 0.53, atol=1e03)

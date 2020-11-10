"""
Hitrate metric:
    * :func:`hitrate`
"""
import torch

from catalyst.metrics.functional import process_recsys


def hitrate(
    outputs: torch.Tensor, targets: torch.Tensor, k=10
) -> torch.Tensor:
    """
    Calculate the hit rate score given model outputs and targets.
    Hit-rate is a metric for evaluating ranking systems.
    Generate top-N recommendations and if one of the recommendation is
    actually what user has rated, you consider that a hit.
    By rate we mean any explicit form of user's interactions.
    Add up all of the hits for all users and then divide by number of users

    Compute top-N recomendation for each user in the training stage
    and intentionally remove one of this items fro the training data.

    Args:
        outputs (torch.Tensor):
            Tensor weith predicted score
            size: [batch_size, slate_length]
            model outputs, logits
        targets (torch.Tensor):
            Binary tensor with ground truth.
            1 means the item is relevant
            for the user and 0 not relevant
            size: [batch_szie, slate_length]
            ground truth, labels
        k (int):
            Parameter fro evaluation on top-k items

    Returns:
        hits_score (torch.Tensor): 
            the hit rate score
    """
    k = min(outputs.size(1), k)
    targets_sorted_by_outputs_at_k = process_recsys(outputs, targets, k)
    hits_score = torch.sum(targets_sorted_by_outputs_at_k, dim=1) / k
    return hits_score


__all__ = ["hitrate"]

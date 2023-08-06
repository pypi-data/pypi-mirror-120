import torch
from katie.rl.softmax_body import SoftmaxBody


def test_softmax_body_creation():
    sb = SoftmaxBody()
    assert (1.0 == sb.temperature)


def test_softmax_body_call():
    sb = SoftmaxBody()
    outputs = torch.tensor([[50, 20, 30, 40]])
    assert (torch.is_tensor(sb(outputs=outputs)))
    assert ((1, 1) == sb(outputs=outputs).shape)
    assert ((1, 3) == sb(outputs=outputs, num_samples=3).shape)

from torch.nn.functional import softmax

"""
SoftmaxBody applies softmax function to the output tensor to generate probabilities of choosing particular output.
The sum of the outputs after softmax application is 1.
"""


class SoftmaxBody:

    def __init__(self, temperature=1.0):
        """
        Constructs the SoftmaxBody object
        :param temperature: the parameter upon which all probabilities will be multiplied before softmax application
        """
        self.temperature = temperature

    def __call__(self, outputs, num_samples=1):
        """
        Generates softmax upon the outputs and based on the probability returns samples.
        :param outputs: the outputs tensor that we want to apply softmax. The shape of outputs should be (1, n).
        If it's not - the exception is thrown.
        :param num_samples: the number of samples that should be taken based on the probability. Defaults to 1.
        If number of samples is longer than length of outputs along the last dimensions,
         the number of samples is set to length of the last dimension.
        :return: indexes of the chosen outputs taken by the probability of this output.
        """
        probabilities = softmax(outputs * self.temperature, dim=1)
        outputs_size = outputs.size()
        if len(outputs_size) != 2:
            raise Exception("The outputs shape should be (m, n)! But instead got {}".format(outputs.shape))
        if num_samples >= outputs_size[-1]:
            return probabilities.multinomial(num_samples=outputs_size[-1])
        else:
            return probabilities.multinomial(num_samples=num_samples)

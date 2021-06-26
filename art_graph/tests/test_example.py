import pytest
import random


@pytest.fixture()
def resource():
    print("setup")
    yield list(range(10))
    print("teardown")


class TestExample:
    def test_shuffle(self, resource):
        # make sure the shuffled sequence does not lose any elements
        seq = resource
        random.shuffle(seq)
        seq.sort()
        assert seq == list(range(10))

        # should raise an exception for an immutable sequence
        with pytest.raises(TypeError):
            immutable = (1, 2, 3)
            random.shuffle(immutable)

    def test_choice(self, resource):
        seq = resource
        element = random.choice(seq)
        assert element in seq

    def test_sample(self, resource):
        seq = resource
        with pytest.raises(ValueError):
            random.sample(seq, 20)
        for element in random.sample(seq, 5):
            assert element in seq

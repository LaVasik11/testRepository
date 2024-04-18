from  unittest import TestCase, main
from work_in_python.work_task.Task_get_score import get_score


class GetScoreTest(TestCase):

    def test_k(self):
        self.assertEqual(get_score([{}, {}], 1000), {})


if __name__ == '__main__':
    main()
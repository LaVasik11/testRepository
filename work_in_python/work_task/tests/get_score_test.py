from unittest import TestCase, main
from work_in_python.work_task.Task_get_score import get_score, generate_game


class GetScoreTest(TestCase):
    game_stamps = generate_game()

    def test_return_data_type(self):
        """Проверяет тип объекта который возврощает функция"""
        self.assertEqual(type(get_score(self.game_stamps, 1000)), type(dict()))

    def test_get_score_initial(self):
        """Проверяет что начальное состояние возвращается при offset <= первой метке"""
        initial_score = self.game_stamps[0]["score"]
        self.assertEqual(get_score(self.game_stamps, 0), initial_score)
        self.assertEqual(get_score(self.game_stamps, -100), initial_score)

    def test_get_score_exact(self):
        """Проверяет что состояние счета возвращается точно в момент заданного offset"""
        for stamp in self.game_stamps:
            offset = stamp["offset"]
            expected_score = stamp["score"]
            self.assertEqual(get_score(self.game_stamps, offset), expected_score)

if __name__ == '__main__':
    main()
M_IN_KM: int = 1000

class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def show_training_info(self):
        training_types: dict = {'SWM': 'Swimming', 'RUN': 'Running', 'WLK': 'SportsWalking'}
        return training_types[self.training_type]()

    def get_message(self):
        return (f'Тип тренировки: {self.training_type};'
                f' Длительность: {round(self.duration, 3)} ч.;'
                f' Дистанция: {round(self.distance, 3)} км;'
                f' Ср. скорость: {round(self.speed, 3)} км/ч;'
                f' Потрачено ккал: {round(self.calories, 3)}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / M_IN_KM

    def get_mean_speed(self, training_time: int) -> float:
        """Получить среднюю скорость движения."""
        distance = self.get_distance()
        return distance / training_time

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage()


class Running(Training):
    """Тренировка: бег."""
    pass


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    pass


class Swimming(Training):
    """Тренировка: плавание."""
    pass


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    pass


def main(training: Training) -> None:
    """Главная функция."""
    pass


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)


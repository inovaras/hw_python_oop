M_IN_KM: int = 1000
HOUR_IN_MIN = 60


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type: str, duration: float, distance: float,
                 speed: float, calories: float) -> None:

        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type};'
                f' Длительность: {round(self.duration, 3)} ч.;'
                f' Дистанция: {round(self.distance, 3)} км;'
                f' Ср. скорость: {round(self.speed, 3)} км/ч;'
                f' Потрачено ккал: {round(self.calories, 3)}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        distance = self.get_distance()
        return distance / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self, training_type: str) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        return InfoMessage(training_type, self.duration, self.get_distance(),
                           self.get_mean_speed(), self.get_spent_calories())
                           # вернуть объект класса сообщения.


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def __init__(self, action: int, duration: float, weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed() +
                 self.CALORIES_MEAN_SPEED_SHIFT) * self.weight / M_IN_KM *
                 self.duration * HOUR_IN_MIN)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_WEIGHT_MULTIPLIER = 0.035
    CALORIES_SQR_SPEED_DIV_HEIGHT_MULTIPLIER = 0.029

    def __init__(self, action: int, duration: float, weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height


    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        return ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight +
                (self.get_mean_speed()**2 / self.height) *
                self.CALORIES_SQR_SPEED_DIV_HEIGHT_MULTIPLIER * self.height)
                * self.duration * HOUR_IN_MIN)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    CALORIES_MEAN_SPEED_MULTIPLIER = 2
    CALORIES_MEAN_SPEED_SHIFT = 1.1

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: int, count_pool: int) -> None:

        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float :
        return self.length_pool * self.count_pool / M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        
        return((self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT) *
                self.CALORIES_MEAN_SPEED_MULTIPLIER * self.weight *
                self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    training_types: dict = {'SWM': Swimming, 'RUN': Running,
                            'WLK': SportsWalking}
    training = training_types[workout_type](*data)
    return training


def main(training: Training) -> None:
    """Главная функция."""

    info = training.show_training_info(training.__doc__)
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

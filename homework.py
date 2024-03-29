from typing import Dict
from typing import List
from typing import Type


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(
        self,
        training_type: str,
        duration: float,
        distance: float,
        speed: float,
        calories: float,
    ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Получить результаты тренировки."""

        return (
            f'Тип тренировки: {self.training_type};'
            f' Длительность: {self.duration :.3f} ч.;'
            f' Дистанция: {self.distance :.3f} км;'
            f' Ср. скорость: {self.speed :.3f} км/ч;'
            f' Потрачено ккал: {self.calories :.3f}.'
        )


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: int = 1000
    MIN_IN_H: int = 60
    LEN_STEP: float = 0.65

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения в км/ч."""

        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            'Определите get_spent_calories в %s.' % self.__class__.__name__
        )

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        return self.create_info_message('Training')

    def create_info_message(self, name: str) -> InfoMessage:
        return InfoMessage(
            name,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        return (
            (
                self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT
            )
            * self.weight
            / self.M_IN_KM
            * self.duration
            * self.MIN_IN_H
        )

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        return self.create_info_message('Running')


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    KMH_IN_MSEC: float = round(Training.M_IN_KM / 3600, 3)
    CM_IN_M: int = 100
    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029

    def __init__(
        self, action: int, duration: float, weight: float, height: float
    ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        avg_speed_m_s = self.get_mean_speed() * self.KMH_IN_MSEC
        return (
            (
                self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                + avg_speed_m_s**2
                / (self.height / self.CM_IN_M)
                * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                * self.weight
            )
            * self.duration
            * Training.MIN_IN_H
        )

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        return self.create_info_message('SportsWalking')


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    CALORIES_MEAN_SPEED_MULTIPLIER = 2
    CALORIES_MEAN_SPEED_SHIFT = 1.1

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: int,
        count_pool: int,
    ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return (
            self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        return (
            (self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
            * self.CALORIES_MEAN_SPEED_MULTIPLIER
            * self.weight
            * self.duration
        )

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        return self.create_info_message('Swimming')


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""

    training_types: Dict[str, training: Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
        'CAT': Cat,
        'DANCE': Dance,
        'NO_TYPE': None,
    }
    return training_types[workout_type](*data)


class Cat:
    def __init__(self, height: int, weight: int) -> None:
        self.height = height
        self.weight = weight


class Dance:
    def __init__(
        self,
        training_type: str,
        duration: float,
        distance: float,
        speed: float,
        calories: float,
    ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories


def main(training) -> None:
    """Главная функция."""

    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
        ('DANCE', [7000, 2, 75, 180]),
        ('CAT', [77, 1, 250, 200]),
        ('INVALID_TYPE', []),
    ]

    for workout_type, data in packages:
        try:
            training = read_package(workout_type, data)
            main(training)
        except KeyError as exc:
            print(
                f'Тренировки {exc} нет в фитнес-трекере :)'
            )
        except TypeError as exc:
            print(
                f'Тренировки {exc} нет в фитнес-трекере :)'
            )
        except AttributeError as exc:
            print(
                f'{exc} нет возможности показать информацию по тренировке '
            )

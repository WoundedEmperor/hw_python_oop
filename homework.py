from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str  # имя класса тренировки
    duration: float  # длительность тренировки
    distance: float  # дистанция тренировки
    speed: float  # средняя скорость во время тренировки
    calories: float  # кол-во ккал, потраченных за тренировку

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


@dataclass
class Training:
    """Базовый класс тренировки."""

    action: int
    duration: float
    weight: float

    LEN_STEP = 0.65  # длина шага (0,65) или гребка (1,38)
    M_IN_KM = 1000  # константа для перевода значений в километры (1000)
    MIN_IN_H = 60
    CALORIES_MEAN_SPEED_MULTIPLIER = 18

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        self.dist = self.action * (self.LEN_STEP) / (self.M_IN_KM)
        return self.dist

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        self.speed = (self.get_distance() / self.duration)
        return self.speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(self.__class__.__name__)

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


@dataclass
class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79
    # получает информаацию:

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self):
        return (((self.CALORIES_MEAN_SPEED_MULTIPLIER) * self.get_mean_speed()
                + (self.CALORIES_MEAN_SPEED_SHIFT)) * self.weight
                / (self.M_IN_KM) * (self.duration * (self.MIN_IN_H)))


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    # принимает параметр height — рост спортсмена
    CALORIES_WEIGHT_MULTIPLIER = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER = 0.029
    KMH_IN_MSEC = 0.278
    CM_IN_M = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action,
                         duration,
                         weight)
        self.height = height

    def get_spent_calories(self):
        return ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                + ((self.get_mean_speed() * self.KMH_IN_MSEC)**2
                 / (self.height / self.CM_IN_M))
                * self.CALORIES_SPEED_HEIGHT_MULTIPLIER * self.weight)
                * self.duration * self.MIN_IN_H)


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38  # переопределить LEN_STEP для этого класса
    CALORIES_MEAN_DURATION_MOD = 1.1
    CALORIES_MEAN_WEIGHT_MOD = 2
    # принимает lenght_pool - длина бассейна
    # принимает count_pool - сколько раз пользователь переплыл бассейн
    # переопределить метод get_spent_calories() и метод get_mean_speed()

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.lenght_pool = length_pool  # длина бассейна в метрах
        self.count_pool = count_pool  # сколько раз переплыл бассейн

    def get_distance(self) -> float:
        swmn_dist = self.LEN_STEP * self.action / self.M_IN_KM
        return swmn_dist

    def get_spent_calories(self) -> float:
        # (средняя_скорость + 1.1) * 2 * вес * время_тренировки
        swmn_cal = ((((self.lenght_pool * self.count_pool)
                    / self.M_IN_KM / self.duration)
                    + self.CALORIES_MEAN_DURATION_MOD)
                    * self.CALORIES_MEAN_WEIGHT_MOD * self.weight
                    * self.duration)
        return swmn_cal

    def get_mean_speed(self):
        swmn = (self.lenght_pool * self.count_pool
                / self.M_IN_KM / self.duration)
        # длина_бассейна * count_pool / M_IN_KM / время_тренировки
        return swmn


def read_package(workout_type: str, data: list[int]) -> Training:
    """Прочитать данные полученные от датчиков."""

    package = {'SWM': Swimming,
               'RUN': Running,
               'WLK': SportsWalking}

    package_type = package[workout_type]
    return package_type(*data)


def main(training: Training) -> None:
    """Главная функция."""
    # принимает на вход экземпляр класса Training,
    # при выполнении функции должен быть вызван метод show_training_info().
    # Результатом должен быть объект IndoMessage,
    # его сохранить в переменную info
    # Для объекта InfoMessage в переменной info должен быть вызван метод,
    # возвращающий строку сообщения с итогом тренировки.
    # строка передаётся в print()
    info: InfoMessage = training.show_training_info()
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

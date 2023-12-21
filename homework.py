from dataclasses import dataclass, field

@dataclass
class Training:
    action: float
    duration: float
    weight: float
    LEN_STEP: float = field(default=0.65, init=False)
    M_IN_KM: int = field(default=1000, init=False)
    MIN_IN_HOUR: int = field(default=60, init=False)

    def get_distance(self) -> float:
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        raise NotImplementedError

    def show_training_info(self) -> 'InfoMessage':
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )

@dataclass
class SportsWalking(Training):
    height: float

    CALORIES_MULTIPLIER1: float = field(default=0.035, init=False)
    CALORIES_MULTIPLIER2: float = field(default=0.029, init=False)
    KMH_TO_MS: float = field(default=0.278, init=False)
    METR_TO_SM: int = field(default=100, init=False)

    def __post_init__(self):
        self.height /= self.METR_TO_SM

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MULTIPLIER1 * self.weight + 
                 ((self.get_mean_speed() * self.KMH_TO_MS) ** 2 / self.height) * 
                 self.CALORIES_MULTIPLIER2 * self.weight) * 
                self.duration * self.MIN_IN_HOUR)


@dataclass
class Swimming(Training):
    length_pool: float
    count_pool: int

    LEN_STEP: float = field(default=1.38, init=False)
    SPEED_KOEF: float = field(default=1.1, init=False)
    SPEED_MULTIPLIER: int = field(default=2, init=False)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.SPEED_KOEF) *
                self.SPEED_MULTIPLIER * self.weight *
                self.duration)

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool / self.M_IN_KM / self.duration)

@dataclass
class Running(Training):
    CALORIES_MEAN_SPEED_MULTIPLIER: int = field(default=18, init=False)
    CALORIES_MEAN_SPEED_SHIFT: float = field(default=1.79, init=False)

    def get_spent_calories(self) -> float:
        return (self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight / self.M_IN_KM * self.duration * self.MIN_IN_HOUR

@dataclass
class InfoMessage:
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self):
        return f"Тип тренировки: {self.training_type}; Длительность: {self.duration:.3f} ч.; Дистанция: {self.distance:.3f} км; Ср. скорость: {self.speed:.3f} км/ч; Потрачено ккал: {self.calories:.3f}."

trainingTypes: dict[str, tuple[type[Training], int]] = {
    'SWM': (Swimming, 5),
    'RUN': (Running, 3),
    'WLK': (SportsWalking, 4),
}

def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type not in trainingTypes:
        raise ValueError(f'Неизвестный тип тренировки: {workout_type}')

    class_, expected = trainingTypes[workout_type]
    if len(data) != expected:
        raise ValueError(f'Некорректное количество аргументов: {data}')

    return class_(*data)

def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
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

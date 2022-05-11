from typing import List


def check_distance(landmark: str, distance_min: int, distance_max: int) -> bool:
    """
    Функция проверяет, входит ли расстояние в указанный диапазон пользователем.
    """
    landmark: List = landmark.split()
    landmark: float = float(landmark[0].replace(',', '.'))
    if float(distance_min) <= landmark <= float(distance_max):
        return True
    else:
        return False

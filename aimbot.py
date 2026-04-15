"""
LoxClient - AIMBOT Module
Minecraft 1.16.5 Java Edition
Автоматическая наводка на врагов
"""

import math
import threading
from typing import Tuple, Optional
from dataclasses import dataclass


@dataclass
class PlayerTarget:
    """Данные цели для наводки"""
    name: str
    x: float
    y: float
    z: float
    head_y: float  # Высота головы
    distance: float


class Aimbot:
    """AIMBOT - автоматический приицел"""
    
    def __init__(self, fov: float = 90.0, smoothness: float = 0.5):
        self.enabled = False
        self.fov = fov  # Field of View (поле зрения)
        self.smoothness = smoothness  # Гладкость наводки (0-1)
        self.current_yaw = 0.0  # Горизонтальный угол
        self.current_pitch = 0.0  # Вертикальный угол
        self.target: Optional[PlayerTarget] = None
        self.aim_thread = None
        
    def calculate_distance(self, x: float, y: float, z: float) -> float:
        """Считает расстояние до цели"""
        return math.sqrt(x**2 + y**2 + z**2)
    
    def calculate_angles(self, target: PlayerTarget) -> Tuple[float, float]:
        """Считает углы для наводки на цель"""
        # Яв (горизонтальный угол)
        yaw = math.degrees(math.atan2(target.z, target.x))
        
        # Питч (вертикальный угол) - наводка на голову
        horizontal_dist = math.sqrt(target.x**2 + target.z**2)
        pitch = math.degrees(math.atan2(target.head_y - target.y, horizontal_dist))
        
        return yaw, pitch
    
    def smooth_aim(self, target_yaw: float, target_pitch: float) -> None:
        """Плавная наводка (чтобы не было видно ботов)"""
        # Интерполяция текущих углов к целевым
        self.current_yaw += (target_yaw - self.current_yaw) * self.smoothness
        self.current_pitch += (target_pitch - self.current_pitch) * self.smoothness
        
        # Нормализация углов
        self.current_yaw = self.current_yaw % 360
        if self.current_pitch > 90:
            self.current_pitch = 90
        elif self.current_pitch < -90:
            self.current_pitch = -90
    
    def find_closest_target(self, players: list) -> Optional[PlayerTarget]:
        """Ищет ближайшую цель в FOV"""
        closest_player = None
        min_distance = float('inf')
        
        for player in players:
            distance = self.calculate_distance(player.x, player.y, player.z)
            
            # Проверяем, в ли цель в нашем FOV
            if distance < min_distance and distance < (self.fov * 10):
                min_distance = distance
                closest_player = player
        
        return closest_player
    
    def aim_loop(self) -> None:
        """Основной цикл наводки"""
        while self.enabled:
            if self.target:
                # Считаем нужные углы
                target_yaw, target_pitch = self.calculate_angles(self.target)
                
                # Плавно наводимся
                self.smooth_aim(target_yaw, target_pitch)
                
                print(f"[AIMBOT] Наводка на {self.target.name}")
                print(f"  Yaw: {self.current_yaw:.1f}° | Pitch: {self.current_pitch:.1f}°")
                print(f"  Расстояние: {self.target.distance:.1f}м\n")
            
            threading.Event().wait(0.01)  # 10ms обновления
    
    def start(self, players: list) -> None:
        """Запускает AIMBOT"""
        self.enabled = True
        self.target = self.find_closest_target(players)
        
        if self.target:
            if not self.aim_thread or not self.aim_thread.is_alive():
                self.aim_thread = threading.Thread(target=self.aim_loop, daemon=True)
                self.aim_thread.start()
            print(f"[AIMBOT] ✓ Активирован на {self.target.name}")
        else:
            print("[AIMBOT] ✗ Целей не найдено")
    
    def stop(self) -> None:
        """Отключает AIMBOT"""
        self.enabled = False
        self.target = None
        print("[AIMBOT] ✗ Деактивирован")
    
    def set_smoothness(self, value: float) -> None:
        """Устанавливает гладкость наводки (0-1)"""
        self.smoothness = max(0.0, min(1.0, value))
        print(f"[AIMBOT] Гладкость: {self.smoothness}")


# Пример использования
if __name__ == "__main__":
    aimbot = Aimbot(fov=90.0, smoothness=0.7)
    
    # Пример данных игроков
    test_players = [
        PlayerTarget("Enemy1", 10, 64, 5, 66, 15),
        PlayerTarget("Enemy2", -8, 64, 12, 66, 18),
    ]
    
    aimbot.start(test_players)
    print("AIMBOT запущен! Нажми Enter для выключения...")
    input()
    aimbot.stop()
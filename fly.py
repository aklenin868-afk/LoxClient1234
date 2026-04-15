class Flight:
    def __init__(self, speed=1.0, altitude=0.0):
        self.speed = speed
        self.altitude = altitude
        self.is_flying = False
        self.position = [0, 0, 0]  # x, y, z coordinates

    def enable_flight(self):
        self.is_flying = True
        print("Flight enabled.")

    def disable_flight(self):
        self.is_flying = False
        print("Flight disabled.")

    def adjust_speed(self, new_speed):
        self.speed = new_speed
        print(f"Speed adjusted to {self.speed}.")

    def maintain_altitude(self):
        if self.is_flying:
            self.position[1] = self.altitude
            print(f"Altitude maintained at {self.altitude}.")

    def detect_collision(self):
        # Example: Placeholder for collision detection logic
        if self.position[1] <= 0:
            print("Collision detected! Altitude too low.")
            self.disable_flight()

    def update_position(self, dx, dy, dz):
        if self.is_flying:
            self.position[0] += dx * self.speed
            self.position[1] += dy * self.speed
            self.position[2] += dz * self.speed
            self.maintain_altitude()
            self.detect_collision()
        print(f"Current position: {self.position}")

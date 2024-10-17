from object import Object
import pygame as pg
import math
import some_math
import constants as const
from time_management import now_milliseconds_since_month as timestamp

def set_objects():
    objects = list()
    image = pg.Surface((100, 100), pg.SRCALPHA)
    pg.draw.circle(image, (255, 0, 0, 255), (50, 50), 50)
    objects.append(Object(image, radius = const.RADIUS,
                                 position = (const.X_0, 0),
                                 speed = const.SPEED,
                                 mass = const.MASS))
    return objects

def set_background():
    background = pg.Surface((800, 500))
    background.fill((255, 255, 255))
    return background

def update_function(self, passed_time, motion_type, air_resistance_type):
    def update_motion_curved(obj, acceleration, resistance, time):
        speed = obj.speed
        coordinates = obj.position
        accel_tang = some_math.projection(acceleration, speed)
        accel_norm = some_math.projection(acceleration, some_math.perpendicular(speed))
        air_accel_abs = resistance(obj)
        moving_clockwise = (math.sin(some_math.to_radians(speed[1] - accel_norm[1])) > 0)
        angle_multyplier = (1 * (not moving_clockwise)) + (-1 * (moving_clockwise))
        radius = (speed[0] ** 2) / accel_norm[0]
        circle_center = some_math.move_point_by_vector(coordinates, (radius, accel_norm[1]))
        circle_len = some_math.circle_length(radius)
        curve_len = (speed[0] * time) + ((accel_tang[0] - air_accel_abs) * (time ** 2) * 0.5)
        curve_angle = 360 * (curve_len / circle_len)
        move_angle = curve_angle * angle_multyplier
        start_point_angle = (some_math.vector_times(accel_norm, -1))[1]
        end_point_angle = start_point_angle + move_angle
        new_coordinates = some_math.move_point_by_vector(circle_center, (radius, end_point_angle))
        new_speed = some_math.sum_vectors([((speed[0] - (air_accel_abs * time)), speed[1]), some_math.vector_times(acceleration, time)])
        return (new_coordinates, new_speed)

    def update_motion_linear(obj, acceleration, resistance, time):
        speed = obj.speed
        coordinates = obj.position
        air_accel_abs = resistance(obj)
        new_speed = some_math.sum_vectors([speed, some_math.vector_times(acceleration, time), some_math.vector_times((-air_accel_abs, speed[1]), time)])
        average_speed = some_math.sum_vectors([some_math.vector_times(speed, 0.5), some_math.vector_times(new_speed, 0.5)])
        shift = some_math.vector_times(average_speed, time)
        new_coordinates = some_math.move_point_by_vector(coordinates, (shift[0], shift[1]))
        return (new_coordinates, new_speed)
    
    update_motion_dict = {'curved': update_motion_curved,
                          'linear': update_motion_linear}

    def air_resistance_linear(object):
        AIR_VISCOSITY = const.ENVIRONMENT_VISCOSITY
        
        force_abs = 6 * math.pi * AIR_VISCOSITY * object.radius * abs(object.speed[0])
        acceleration_abs = force_abs / object.mass

        return acceleration_abs
    
    def air_resistance_quadratic(object):
        AIR_DENSITY = const.ENVIRONMENT_DENSITY
        DRAG_COEFFICIENT = const.DRAG_COEFFICIENT

        reference_area = math.pi * (object.radius ** 2)
        force_abs = 0.5 * AIR_DENSITY * (object.speed[0] ** 2) * DRAG_COEFFICIENT * reference_area
        acceleration_abs = force_abs / object.mass
        
        return acceleration_abs
    
    air_resistance_dict = {'linear': air_resistance_linear,
                           'quadratic': air_resistance_quadratic}

    MIN_Y_POSITION = -const.HEIGHT

    accelerators = [const.GRAVITATIONAL_ACCELERATION]
    acceleration = some_math.sum_vectors(accelerators)
    sec_time = passed_time / 1000

    update_motion = update_motion_dict.get(motion_type, update_motion_linear)
    air_resistance = air_resistance_dict.get(air_resistance_type, air_resistance_linear)

    for obj in self.objects:
        if ((obj.position)[1] > MIN_Y_POSITION):
            obj.position, obj.speed = update_motion(obj, acceleration, air_resistance, sec_time)
            obj.last_acceleration = acceleration

            if (self.process_state == -1):
                self.process_state = 0
                self.begin_time = timestamp()
        elif (self.process_state != 1):
            obj.last_acceleration = (0, 0)
            self.process_state = 1
            self.end_time = timestamp()


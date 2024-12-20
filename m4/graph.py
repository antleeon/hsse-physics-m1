import constants as const
import math as m
import some_math as sm
import matplotlib.pyplot as plt
import theory_calculations as calc
import pendulum

from object import Object
from process import Process

ANGLE_INTERVAL = (0, 80)
POINTS_QUANTITY = 500
OBJECT_OPTION = 'ball'
ENVIRONMENT_OPTION = 'Earth, air'

def find_real_period(res: dict) -> float:
    attachment = res['attachment']
    speed = res['speed']
    
    object = pendulum.set_object(OBJECT_OPTION, speed, attachment)
    process = pendulum.set_process(ENVIRONMENT_OPTION, [object], 1, (100, 100), (50, 50), f'')

    real_period = pendulum.get_real_period(process)

    return real_period

if (__name__ == '__main__'):
    angle_points = list()
    
    theory_points = list()
    real_points = list()
    harmonic_points = list()

    for i in range(POINTS_QUANTITY):
        ang = ANGLE_INTERVAL[0] + (((ANGLE_INTERVAL[1] - ANGLE_INTERVAL[0]) / (POINTS_QUANTITY - 1)) * i)
        angle_points.append(abs(ang) * 2)
        const.ANGLE = ang
        #const.ANGULAR_VELOCITY = 0

        theory_res = calc.count(ENVIRONMENT_OPTION, OBJECT_OPTION, True)
        
        theory_period = theory_res['real period']
        real_period = find_real_period(theory_res)
        harmonic_period = theory_res['period']

        theory_points.append(theory_period)
        real_points.append(real_period)
        harmonic_points.append(harmonic_period)

    print('Graph points calculated') # debug

    plt.plot(angle_points, theory_points)
    plt.plot(angle_points, real_points)
    plt.plot(angle_points, harmonic_points)
    plt.title('Period to amplitude relation')
    plt.xlabel('Angle amplitude, degrees')
    plt.ylabel('Period, seconds')
    plt.grid()
    plt.legend(['theoretical', 'real', 'harmonic'])
    plt.show()
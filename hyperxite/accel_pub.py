import random, rclpy
from rclpy.node import Node
from std_msgs.msg import UInt16MultiArray

import board, busio
i2c = busio.I2C(board.SCL, board.SDA)
import adafruit_ads1x15.ads1015 as ADS

from adafruit_ads1x15.analog_in  import AnalogIn
ads = ADS.ADS1015(i2c)

class AccelPublisher(Node):

    def __init__(self):
        super().__init__('accel_publisher')
        self.publisher_ = self.create_publisher(UInt16MultiArray, 'accelerometer', 10)
        timer_period = 0.5
        self.timer = self.create_timer(timer_period, self.timer_callback)
        
    def timer_callback(self):
        chanX = AnalogIn(ads, ADS.P0)
        chanY = AnalogIn(ads, ADS.P1)
        chanZ = AnalogIn(ads, ADS.P2)

        msg = UInt16MultiArray()
        msg.data = [chanX.value,chanY.value,chanZ.value]
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%d"' % msg.data[0])

def main(args=None):
    rclpy.init(args=args)

    accel_publisher = AccelPublisher()

    rclpy.spin(accel_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    accel_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
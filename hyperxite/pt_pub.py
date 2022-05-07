import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray

import board, busio
i2c = busio.I2C(board.SCL, board.SDA)
from adafruit_ina219 import ADCResolution, BusVoltageRange, INA219

ina219A = INA219(i2c, 0x40)


class PTPublisher(Node):
    
    def __init__(self):
        super().__init__('pt_publisher')
        self.publisher_ = self.create_publisher(Float32MultiArray, 'pressure_transducers', 10)
        timer_period = 0.5
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        curr1 = ina219A.current

        msg = Float32MultiArray()
        msg.data = [curr1]
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%d"' % msg.data[0])


def main(args=None):
    rclpy.init(args=args)

    pt_publisher = PTPublisher()

    rclpy.spin(pt_publisher)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
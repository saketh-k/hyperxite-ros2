import random, rclpy
from rclpy.node import Node
from std_msgs.msg import String
import serial

ser = serial.Serial('/dev/ttyUSB0')  # open serial port


class BMSPublisher(Node):

    def __init__(self):
        super().__init__('bms_publisher')
        self.publisher_ = self.create_publisher(String, 'bms', 10)
        timer_period = 0.5
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.ser = serial.Serial('/dev/ttyUSB0')
        self.ser.write(b'S5\r')
        self.ser.write(b'O\r')
        self.get_logger().info('Connected on port: '+ self.ser.name)

        
    def timer_callback(self):
        data = self.ser.read_until(b'\r')

        msg = String
        msg.data = data
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: ' + msg.data)

def main(args=None):
    rclpy.init(args=args)

    bms_publisher = BMSPublisher()

    rclpy.spin(bms_publisher)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
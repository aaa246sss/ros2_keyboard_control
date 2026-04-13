import rospy
from geometry_msgs.msg import Twist
import sys
import select
import tty
import termios
import time

class KeyboardController:
    def __init__(self):
        rospy.init_node('keyboard_controller')
        self.publisher_ = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.publisher1_ = rospy.Publisher('/cmd_vel1', Twist, queue_size=10)
        self.rate = rospy.Rate(20)  # 20Hz，相当于0.05秒
        
        # 速度参数
        self.max_linear_velocity = 0.5  # 最大线速度
        self.max_angular_velocity = 1.0  # 最大角速度
        self.acceleration = 0.1  # 加速度
        
        # 当前速度
        self.current_linear_x = 0.0
        self.current_angular_z = 0.0
        
        # 目标速度
        self.target_linear_x = 0.0
        self.target_angular_z = 0.0
        
        # 键盘输入设置
        self.settings = termios.tcgetattr(sys.stdin)
        self.key = ''
        
        # 按键状态跟踪
        self.last_key = ''
        self.last_key_time = time.time()
        self.key_release_timeout = 0.5  # 按键松开的超时时间（秒）
        
        # 发布标志
        self.zero_velocity_published = False
        
        print('This node takes keypresses from the keyboard and publishes them')
        print('as Twist messages. It works best with a US keyboard layout.')
        print('---------------------------')
        print('Moving around:')
        print('   u    i    o')
        print('   j    k    l')
        print('   m    ,    .')
        print('')
        print('For Holonomic mode (strafing), hold down the shift key:')
        print('---------------------------')
        print('   U    I    O')
        print('   J    K    L')
        print('   M    <    >')
        print('')
        print('t : up (+z)')
        print('b : down (-z)')
        print('')
        print('anything else : stop')
        print('')
        print('q/z : increase/decrease max speeds by 10%')
        print('w/x : increase/decrease only linear speed by 10%')
        print('e/c : increase/decrease only angular speed by 10%')
        print('r/v : increase/decrease acceleration')
        print('')
        print('p : publish zero velocity to /cmd_vel1')
        print('')
        print('CTRL-C to quit')
        print('')
        print(f'currently: \t speed {self.max_linear_velocity} \t turn {self.max_angular_velocity} \t accel {self.acceleration}')
    
    def getKey(self):
        # 保存当前终端设置
        old_settings = termios.tcgetattr(sys.stdin)
        try:
            # 设置终端为raw模式，不回显输入
            tty.setraw(sys.stdin.fileno())
            rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
            if rlist:
                key = sys.stdin.read(1)
                # 检测Ctrl+C
                if key == '\x03':
                    raise KeyboardInterrupt
            else:
                key = ''
        finally:
            # 恢复终端设置
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
        return key
    
    def timer_callback(self):
        # 获取键盘输入
        self.key = self.getKey()
        
        # 处理键盘输入
        current_time = time.time()
        
        # 检查是否有按键输入
        if self.key != '':
            # 有按键输入，更新按键状态
            if self.key != self.last_key:
                self.last_key = self.key
                self.last_key_time = current_time
            else:
                # 同一按键持续按下，更新时间
                self.last_key_time = current_time
            
            # 处理按键输入
            if self.key == 'i':  # 前进
                self.target_linear_x = self.max_linear_velocity
                self.target_angular_z = 0.0
            elif self.key == ',':  # 后退
                self.target_linear_x = -self.max_linear_velocity
                self.target_angular_z = 0.0
            elif self.key == 'j':  # 左转
                self.target_linear_x = 0.0
                self.target_angular_z = self.max_angular_velocity
            elif self.key == 'l':  # 右转
                self.target_linear_x = 0.0
                self.target_angular_z = -self.max_angular_velocity
            elif self.key == 'u':  # 前进左转
                self.target_linear_x = self.max_linear_velocity
                self.target_angular_z = self.max_angular_velocity
            elif self.key == 'o':  # 前进右转
                self.target_linear_x = self.max_linear_velocity
                self.target_angular_z = -self.max_angular_velocity
            elif self.key == 'm':  # 后退左转
                self.target_linear_x = -self.max_linear_velocity
                self.target_angular_z = self.max_angular_velocity
            elif self.key == '.':  # 后退右转
                self.target_linear_x = -self.max_linear_velocity
                self.target_angular_z = -self.max_angular_velocity
            elif self.key == 'U':  # 右移
                self.target_linear_x = 0.0
                self.target_angular_z = 0.0
            elif self.key == 'I':  # 前右移
                self.target_linear_x = self.max_linear_velocity
                self.target_angular_z = 0.0
            elif self.key == 'O':  # 左移
                self.target_linear_x = 0.0
                self.target_angular_z = 0.0
            elif self.key == 'J':  # 左平移
                self.target_linear_x = 0.0
                self.target_angular_z = 0.0
            elif self.key == 'L':  # 右平移
                self.target_linear_x = 0.0
                self.target_angular_z = 0.0
            elif self.key == 'M':  # 后左移
                self.target_linear_x = -self.max_linear_velocity
                self.target_angular_z = 0.0
            elif self.key == '<':  # 后移
                self.target_linear_x = -self.max_linear_velocity
                self.target_angular_z = 0.0
            elif self.key == '>':  # 后右移
                self.target_linear_x = -self.max_linear_velocity
                self.target_angular_z = 0.0
            elif self.key == 't':  # 上移
                self.target_linear_x = 0.0
                self.target_angular_z = 0.0
            elif self.key == 'b':  # 下移
                self.target_linear_x = 0.0
                self.target_angular_z = 0.0
            elif self.key == 'q':  # 增加最大速度10%
                self.max_linear_velocity *= 1.1
                self.max_angular_velocity *= 1.1
                print(f'currently: \t speed {self.max_linear_velocity:.2f} \t turn {self.max_angular_velocity:.2f} \t accel {self.acceleration:.2f}')
            elif self.key == 'z':  # 减少最大速度10%
                self.max_linear_velocity *= 0.9
                self.max_angular_velocity *= 0.9
                print(f'currently: \t speed {self.max_linear_velocity:.2f} \t turn {self.max_angular_velocity:.2f} \t accel {self.acceleration:.2f}')
            elif self.key == 'w':  # 只增加线性速度10%
                self.max_linear_velocity *= 1.1
                print(f'currently: \t speed {self.max_linear_velocity:.2f} \t turn {self.max_angular_velocity:.2f} \t accel {self.acceleration:.2f}')
            elif self.key == 'x':  # 只减少线性速度10%
                self.max_linear_velocity *= 0.9
                print(f'currently: \t speed {self.max_linear_velocity:.2f} \t turn {self.max_angular_velocity:.2f} \t accel {self.acceleration:.2f}')
            elif self.key == 'e':  # 只增加角速度10%
                self.max_angular_velocity *= 1.1
                print(f'currently: \t speed {self.max_linear_velocity:.2f} \t turn {self.max_angular_velocity:.2f} \t accel {self.acceleration:.2f}')
            elif self.key == 'c':  # 只减少角速度10%
                self.max_angular_velocity *= 0.9
                print(f'currently: \t speed {self.max_linear_velocity:.2f} \t turn {self.max_angular_velocity:.2f} \t accel {self.acceleration:.2f}')
            elif self.key == 'r':  # 增加加速度
                self.acceleration += 0.01
                print(f'Acceleration increased to: {self.acceleration:.2f}')
            elif self.key == 'v':  # 减少加速度
                self.acceleration = max(0.01, self.acceleration - 0.01)
                print(f'Acceleration decreased to: {self.acceleration:.2f}')
            elif self.key == 'k' or self.key == ' ':  # 停止
                self.target_linear_x = 0.0
                self.target_angular_z = 0.0
            elif self.key == 'p':  # 发布零速度到/cmd_vel1
                self.publish_zero_velocity()
        else:
            # 没有按键输入，检查是否超过了按键松开的超时时间
            if current_time - self.last_key_time > self.key_release_timeout:
                # 超过超时时间，将目标速度设置为0
                self.target_linear_x = 0.0
                self.target_angular_z = 0.0
        
        # 梯形加减速
        self.apply_acceleration()
        
        # 发布速度命令
        self.publish_velocity()
    
    def apply_acceleration(self):
        # 线速度加减速
        if self.current_linear_x < self.target_linear_x:
            self.current_linear_x = min(self.target_linear_x, self.current_linear_x + self.acceleration)
        elif self.current_linear_x > self.target_linear_x:
            # 当目标速度为0时，确保能够精确停止到0
            if self.target_linear_x == 0.0:
                if abs(self.current_linear_x) <= self.acceleration:
                    self.current_linear_x = 0.0
                else:
                    self.current_linear_x = max(self.target_linear_x, self.current_linear_x - self.acceleration)
            else:
                self.current_linear_x = max(self.target_linear_x, self.current_linear_x - self.acceleration)
        
        # 角速度加减速（角加速度是线加速度的2倍）
        angular_acceleration = self.acceleration * 2.0
        if self.current_angular_z < self.target_angular_z:
            self.current_angular_z = min(self.target_angular_z, self.current_angular_z + angular_acceleration)
        elif self.current_angular_z > self.target_angular_z:
            # 当目标速度为0时，确保能够精确停止到0
            if self.target_angular_z == 0.0:
                if abs(self.current_angular_z) <= angular_acceleration:
                    self.current_angular_z = 0.0
                else:
                    self.current_angular_z = max(self.target_angular_z, self.current_angular_z - angular_acceleration)
            else:
                self.current_angular_z = max(self.target_angular_z, self.current_angular_z - angular_acceleration)
    
    def publish_velocity(self):
        # 当速度不为0时发布消息
        # 当目标速度为0且当前速度正在趋近于0时，继续发布直到真正达到0
        # 当速度为0时，发布一次全0的消息，然后停止发布
        if (abs(self.current_linear_x) > 0.0 or abs(self.current_angular_z) > 0.0):
            msg = Twist()
            # 当速度非常接近0时，直接设置为0.0
            if abs(self.current_linear_x) < 1e-6:
                msg.linear.x = 0.0
            else:
                msg.linear.x = self.current_linear_x
            if abs(self.current_angular_z) < 1e-6:
                msg.angular.z = 0.0
            else:
                msg.angular.z = self.current_angular_z
            self.publisher_.publish(msg)
            # 重置零速度发布标志
            self.zero_velocity_published = False
        elif (self.target_linear_x == 0.0 and self.target_angular_z == 0.0 and not self.zero_velocity_published):
            # 当目标速度为0且当前速度已经为0时，发布一次全0的消息，然后停止
            msg = Twist()
            msg.linear.x = 0.0
            msg.linear.y = 0.0
            msg.linear.z = 0.0
            msg.angular.x = 0.0
            msg.angular.y = 0.0
            msg.angular.z = 0.0
            self.publisher_.publish(msg)
            # 设置零速度已发布标志
            self.zero_velocity_published = True
    
    def publish_zero_velocity(self):
        msg = Twist()
        msg.linear.x = 0.0
        msg.linear.y = 0.0
        msg.linear.z = 0.0
        msg.angular.x = 0.0
        msg.angular.y = 0.0
        msg.angular.z = 0.0
        self.publisher1_.publish(msg)
        print('Published zero velocity to /cmd_vel1')
    
    def run(self):
        while not rospy.is_shutdown():
            self.timer_callback()
            self.rate.sleep()

def main():
    keyboard_controller = KeyboardController()
    
    try:
        keyboard_controller.run()
    except KeyboardInterrupt:
        pass
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, keyboard_controller.settings)

if __name__ == '__main__':
    main()
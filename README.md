# ROS2 Keyboard Controller

ROS2键盘控制节点，用于控制机器人的移动，支持梯形加减速和双topic发布功能。

## 功能特性

- **基本控制**：使用i/,/j/l键控制机器人前后左右移动
- **梯形加减速**：实现平滑的速度过渡效果，角加速度是线加速度的2倍
- **加速度调节**：通过r/v键调整加速度大小
- **双topic发布**：
  - `/cmd_vel`：发布带有加减速的速度命令
  - `/cmd_vel1`：按p键时发布全0的速度命令
- **速度调整**：通过q/z/w/x/e/c键调整最大速度
- **零速度停止**：速度为0时停止发布/cmd_vel topic
- **按键松开自动减速**：松开按键300ms后自动将速度降到0
- **隐藏按键输入**：长按按键不会在终端显示字符，保持终端整洁
- **正常退出**：支持Ctrl+C正常退出节点，不会导致终端显示乱码

## 控制键位

```
Moving around:
   u    i    o
   j    k    l
   m    ,    .

For Holonomic mode (strafing), hold down the shift key:
---------------------------
   U    I    O
   J    K    L
   M    <    >

t : up (+z)
b : down (-z)

k or space : stop

q/z : increase/decrease max speeds by 10%
w/x : increase/decrease only linear speed by 10%
e/c : increase/decrease only angular speed by 10%
r/v : increase/decrease acceleration

p : publish zero velocity to /cmd_vel1

CTRL-C to quit
```

## 安装和运行

### 依赖项
- ROS2 Galactic
- Python3
- rclpy
- geometry_msgs

### 构建项目

```bash
cd ros2_keyboard_control
source /opt/ros/galactic/setup.bash
colcon build
```

### 运行节点

```bash
source install/setup.bash
ros2 run keyboard_controller keyboard_node
```

## 测试

1. 启动键盘控制节点
2. 在另一个终端中订阅topic：
   - `ros2 topic echo /cmd_vel`
   - `ros2 topic echo /cmd_vel1`
3. 测试各种控制键位，观察速度变化和加减速效果
4. 长按i键，观察速度是否连续增加，不再出现卡顿
5. 松开按键，观察300ms后速度是否逐渐降到0
6. 按p键，观察/cmd_vel1是否发布全0数据
7. 按r和v键，调节加速度大小，观察current行显示的加速度值变化
8. 按Ctrl+C，测试节点是否能够正常退出，终端是否不再显示乱码

## 项目结构

```
ros2_keyboard_control/
├── .trae/
│   └── documents/
│       └── keyboard_controller_plan.md
├── src/
│   └── keyboard_controller/
│       ├── keyboard_controller/
│       │   ├── __init__.py
│       │   └── keyboard_node.py
│       ├── resource/
│       │   └── keyboard_controller
│       ├── test/
│       │   ├── test_copyright.py
│       │   ├── test_flake8.py
│       │   └── test_pep257.py
│       ├── package.xml
│       ├── setup.cfg
│       └── setup.py
├── .gitignore
└── README.md
```

## 技术实现

1. **梯形加减速**：通过逐步调整当前速度到目标速度，实现平滑的加减速效果
2. **角加速度**：角加速度是线加速度的2倍，确保转向更加灵活
3. **按键状态跟踪**：通过跟踪按键的按下和松开状态，实现长按连续加速和松开后自动减速
4. **双topic发布**：支持发布速度命令到两个不同的topic，满足不同的控制需求
5. **终端设置**：在节点启动时设置终端为raw模式，避免按键回显，在退出时恢复终端设置，确保终端正常工作

## 注意事项

- 该节点使用的是US键盘布局，其他键盘布局可能需要调整键位
- 确保在运行节点前已经正确设置了ROS2环境
- 若终端在退出节点后显示异常，可以尝试运行`reset`命令恢复终端设置
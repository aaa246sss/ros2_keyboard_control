# ROS2键盘控制节点 - 实现计划

## 项目概述
创建一个ROS2工程，使用Python3编写键盘控制节点，实现基本的移动控制、梯形加减速功能，以及双topic发布功能。

## 任务分解

### [x] 任务1: 创建ROS2工程目录结构
- **Priority**: P0
- **Depends On**: None
- **Description**:
  - 创建主工程目录 `ros2_keyboard_control`
  - 在工程目录下创建 `src` 目录
- **Success Criteria**:
  - 目录结构正确创建
- **Test Requirements**:
  - `programmatic` TR-1.1: 目录结构存在且正确

### [x] 任务2: 创建ROS2 Python包
- **Priority**: P0
- **Depends On**: 任务1
- **Description**:
  - 在 `src` 目录下创建名为 `keyboard_controller` 的Python包
  - 使用 `ros2 pkg create` 命令创建包结构
- **Success Criteria**:
  - Python包创建成功，包含必要的文件结构
- **Test Requirements**:
  - `programmatic` TR-2.1: 包结构完整，包含 package.xml、setup.py 等文件

### [x] 任务3: 实现键盘控制节点代码
- **Priority**: P0
- **Depends On**: 任务2
- **Description**:
  - 创建 `keyboard_node.py` 文件
  - 实现键盘输入处理
  - 实现基本的前后左右控制（i/j/k/l键）
  - 实现梯形加减速功能
  - 实现加速度调节功能（w/s键）
  - 实现/cmd_vel topic发布
  - 实现按p键发布全0数据到/cmd_vel1 topic
- **Success Criteria**:
  - 代码实现完整，包含所有要求的功能
- **Test Requirements**:
  - `programmatic` TR-3.1: 代码编译通过
  - `human-judgement` TR-3.2: 代码结构清晰，注释完整

### [x] 任务4: 配置package.xml文件
- **Priority**: P1
- **Depends On**: 任务2
- **Description**:
  - 添加必要的依赖项：rclpy 和 geometry_msgs
- **Success Criteria**:
  - package.xml 配置正确，包含所有必要的依赖
- **Test Requirements**:
  - `programmatic` TR-4.1: 依赖项配置正确

### [x] 任务5: 配置setup.py文件
- **Priority**: P1
- **Depends On**: 任务2
- **Description**:
  - 添加键盘节点的入口点
- **Success Criteria**:
  - setup.py 配置正确，包含节点入口点
- **Test Requirements**:
  - `programmatic` TR-5.1: 入口点配置正确

### [x] 任务6: 构建ROS2工程
- **Priority**: P0
- **Depends On**: 任务3、4、5
- **Description**:
  - 使用 `colcon build` 命令构建工程
- **Success Criteria**:
  - 工程构建成功，无编译错误
- **Test Requirements**:
  - `programmatic` TR-6.1: 构建过程无错误

## 功能说明

### 控制键位
- **i**: 前进
- **,**: 后退
- **j**: 左转
- **l**: 右转
- **k** 或 **空格**: 停止
- **p**: 发布全0数据到/cmd_vel1
- **w**: 增加加速度
- **s**: 减少加速度

### 技术实现
1. **梯形加减速**：通过逐步调整当前速度到目标速度，实现平滑的加减速效果
2. **双topic发布**：
   - `/cmd_vel`：发布带有加减速的速度命令
   - `/cmd_vel1`：按p键时发布全0的速度命令
3. **加速度调节**：通过w和s键可以实时调整加速度大小

## 测试方法
1. 启动ROS2环境：`source /opt/ros/galactic/setup.bash`
2. 启动键盘控制节点：`ros2 run keyboard_controller keyboard_node`
3. 在另一个终端中订阅topic：
   - `ros2 topic echo /cmd_vel`
   - `ros2 topic echo /cmd_vel1`
4. 测试各种控制键位，观察速度变化和加减速效果
5. 按p键，观察/cmd_vel1是否发布全0数据

## 依赖项
- ROS2 Galactic
- Python3
- rclpy
- geometry_msgs
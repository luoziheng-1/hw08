import pybullet as p
import pybullet_data
import time

# 连接GUI
p.connect(p.GUI)

# 设置资源路径
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# 设置重力
p.setGravity(0, 0, -9.8)

# 加载地面
plane = p.loadURDF("plane.urdf")

# 加载Panda机械臂
robot = p.loadURDF(
    "franka_panda/panda.urdf",
    useFixedBase=True
)

# 加载方块
cube = p.loadURDF(
    "cube_small.urdf",
    [0.6, 0.0, 0.02]
)

# 增大摩擦
p.changeDynamics(
    cube,
    -1,
    lateralFriction=10
)

# 控制机械臂运动
def move_to(target):

    jointPoses = p.calculateInverseKinematics(
        robot,
        11,
        target
    )

    for _ in range(300):

        for j in range(7):

            p.setJointMotorControl2(
                robot,
                j,
                p.POSITION_CONTROL,
                targetPosition=jointPoses[j]
            )

        p.stepSimulation()
        time.sleep(1/240)


# 打开夹爪
def open_gripper():

    for _ in range(100):

        p.setJointMotorControl2(
            robot,
            9,
            p.POSITION_CONTROL,
            targetPosition=0.04,
            force=100
        )

        p.setJointMotorControl2(
            robot,
            10,
            p.POSITION_CONTROL,
            targetPosition=0.04,
            force=100
        )

        p.stepSimulation()
        time.sleep(1/240)


# 闭合夹爪
def close_gripper():

    for _ in range(100):

        p.setJointMotorControl2(
            robot,
            9,
            p.POSITION_CONTROL,
            targetPosition=0.0,
            force=300
        )

        p.setJointMotorControl2(
            robot,
            10,
            p.POSITION_CONTROL,
            targetPosition=0.0,
            force=300
        )

        p.stepSimulation()
        time.sleep(1/240)


# 初始稳定
for _ in range(100):
    p.stepSimulation()

# 打开夹爪
open_gripper()

# 1. 移动到方块上方
move_to([0.6, 0.0, 0.25])

# 2. 下降
move_to([0.6, 0.0, 0.05])

# 3. 闭合夹爪
close_gripper()

# 4. 创建固定约束（模拟成功抓取）
constraint_id = p.createConstraint(
    parentBodyUniqueId=robot,
    parentLinkIndex=11,
    childBodyUniqueId=cube,
    childLinkIndex=-1,
    jointType=p.JOINT_FIXED,
    jointAxis=[0, 0, 0],
    parentFramePosition=[0, 0, 0],
    childFramePosition=[0, 0, 0]
)

# 5. 抬起
move_to([0.6, 0.0, 0.35])

# 6. 移动到新位置
move_to([0.3, 0.3, 0.35])

# 7. 放下
move_to([0.3, 0.3, 0.05])

# 8. 释放方块
p.removeConstraint(constraint_id)

# 9. 打开夹爪
open_gripper()

# 10. 机械臂抬起
move_to([0.3, 0.3, 0.35])

print("任务完成：方块已搬运到新位置")

# 保持窗口
while True:
    p.stepSimulation()
    time.sleep(1/240)
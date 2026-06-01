import pybullet as p
import pybullet_data
import time

# 连接仿真器
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.8)

# 加载场景
plane = p.loadURDF("plane.urdf")

robot = p.loadURDF(
    "franka_panda/panda.urdf",
    useFixedBase=True
)

# 加载方块
cube = p.loadURDF(
    "cube_small.urdf",
    [0.6, 0, 0.02]
)

# 打开夹爪
for joint in [9, 10]:
    p.setJointMotorControl2(
        robot,
        joint,
        p.POSITION_CONTROL,
        targetPosition=0.04,
        force=100
    )

# 第一目标：移动到方块上方
target1 = [0.6, 0, 0.25]

jointPoses = p.calculateInverseKinematics(
    robot,
    11,
    target1
)

for _ in range(200):
    for j in range(7):
        p.setJointMotorControl2(
            robot,
            j,
            p.POSITION_CONTROL,
            jointPoses[j]
        )
    p.stepSimulation()
    time.sleep(1/240)

# 第二目标：下降到方块
target2 = [0.6, 0, 0.05]

jointPoses = p.calculateInverseKinematics(
    robot,
    11,
    target2
)

for _ in range(200):
    for j in range(7):
        p.setJointMotorControl2(
            robot,
            j,
            p.POSITION_CONTROL,
            jointPoses[j]
        )
    p.stepSimulation()
    time.sleep(1/240)

# 闭合夹爪
for _ in range(200):
    p.setJointMotorControl2(
        robot,
        9,
        p.POSITION_CONTROL,
        targetPosition=0,
        force=200
    )
    p.setJointMotorControl2(
        robot,
        10,
        p.POSITION_CONTROL,
        targetPosition=0,
        force=200
    )
    p.stepSimulation()
    time.sleep(1/240)
constraint_id = p.createConstraint(
    parentBodyUniqueId=robot,
    parentLinkIndex=11,      # Panda末端执行器
    childBodyUniqueId=cube,
    childLinkIndex=-1,
    jointType=p.JOINT_FIXED,
    jointAxis=[0,0,0],
    parentFramePosition=[0,0,0],
    childFramePosition=[0,0,0]
)

# 抬起方块
target3 = [0.6, 0, 0.35]

jointPoses = p.calculateInverseKinematics(
    robot,
    11,
    target3
)

for _ in range(300):
    for j in range(7):
        p.setJointMotorControl2(
            robot,
            j,
            p.POSITION_CONTROL,
            jointPoses[j]
        )
    p.stepSimulation()
    time.sleep(1/240)

print("抓取完成")

while True:
    p.stepSimulation()
    time.sleep(1/240)
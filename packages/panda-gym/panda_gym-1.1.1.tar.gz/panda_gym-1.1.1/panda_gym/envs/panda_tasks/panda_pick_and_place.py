from panda_gym.envs.core import RobotTaskEnv
from panda_gym.pybullet import PyBullet
from panda_gym.envs.robots import Panda
from panda_gym.envs.tasks import PickAndPlace


class PandaPickAndPlaceEnv(RobotTaskEnv):
    """Pick and Place task wih Panda robot.

    Args:
        render (bool, optional): Activate rendering. Defaults to False.
        reward_type (str, optional): "sparse" or "dense". Defaults to "sparse".
    """

    def __init__(self, render=False, reward_type="sparse"):
        self.sim = PyBullet(render=render)
        self.robot = Panda(
            self.sim,
            block_gripper=False,
            base_position=[-0.6, 0.0, 0.0],
            fingers_friction=5.0,
        )
        self.task = PickAndPlace(self.sim, reward_type=reward_type)
        RobotTaskEnv.__init__(self)

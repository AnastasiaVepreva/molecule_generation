from baselines.baselines.deepq import models  # noqa
from baselines.baselines.deepq.build_graph import build_act, build_train  # noqa
from baselines.baselines.deepq.deepq import learn, load_act  # noqa
from baselines.baselines.deepq.replay_buffer import ReplayBuffer, PrioritizedReplayBuffer  # noqa

def wrap_atari_dqn(env):
    from baselines.baselines.common.atari_wrappers import wrap_deepmind
    return wrap_deepmind(env, frame_stack=True, scale=False)

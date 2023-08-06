import os
import gym
from gym import spaces
import numpy as np
import random
import pandas as pd
import tensorflow as tf
import itertools
from ta import momentum, volume


class TradeEnv(gym.Env):
    def __init__(self, market="Brasil", old_dataset=False):

        # self.strategy = strategy
        self.market = market
        self.codes = ["VIIA3.SA", "OIBR3.SA", "ABEV3.SA"]

        self.old_dataset = old_dataset

        # Amount of steps before resetting the training environment
        self.episode_length = 1000
        self.training_steps = 0

        self.features = ['adj close', 'rsi', 'mfi', 'kama']
        self.path = ['full_data', 'windowed_data/test', 'windowed_data/train']
        self.filenames = ['test', 'train']
        self.format_file = '.tfrecord'
        self.file_save_counter = 1
        self.portfolio_size = len(self.codes) + 1
        self.iterator = 0

        # The window for which each series of data will be generated in order to train our agent.
        self.window_length = 128

        # The agent can either buy, or sell a percentage of each share [0, 1].
        self.action_space = spaces.Box(low=np.float32(0), high=np.float32(1),
                                       shape=(self.portfolio_size,), dtype=np.float32)

        # The observation space follows the shape of the states, (window_length, (num_codes*4)), 4 is the number of
        # indicators used in each code (rsi, obv and kama) + the prices of the assets themselves
        self.observation_space = spaces.Box(low=np.float32(0), high=np.float32(3),
                                            shape=(self.window_length, (self.portfolio_size - 1) * 4),
                                            dtype=np.float32)

        # The weights of the shares owned (at the moment or previously).
        # The index 0 is always the free risk investment.
        self.weights = [1] + list(np.zeros(len(self.codes)))

        # Starting money for investments.
        self.starting_money = 7000
        self.money = self.starting_money
        self.share_count = list(np.zeros(self.portfolio_size))
        self.data = 0

        self.train_states = []
        self.train_price_history = []
        self.test_states = []
        self.test_price_history = []
        self.tf_train_states = []
        self.tf_test_states = []

        self.states = []
        self.price_history = []
        self.total_steps = 0
        self.total_reward = 0
        self.reward_scale = 100 / self.starting_money

        self.current_state = []
        self.current_prices = pd.DataFrame()
        self.max_steps = 0
        self.done = True
        self.base_price = 0

        self.feature_description = 0
        self.previous_money = 0

    def step(self, action, random_test=False):
        # print(action)
        if self.done:
            self.reset()

        if np.sum(action) == 0:
            # Penalize the agent for sending an empty list of weights.
            reward = -1

            self.total_steps += 1

            if self.total_steps == self.max_steps or self.total_steps == self.training_steps:
                self.done = True

            self.current_state, self.current_prices = self.get_next_state(), \
                                                      self.price_history[self.total_steps - 1]

            self.total_reward += reward * self.reward_scale

        else:
            if random_test:
                action = self.normalized_sample(action)
            else:
                action = self.normalized_action(action)

            self.weights = [.2 * i for i in self.weights]

            self.weights = [x + y for (x, y) in zip(list(self.weights), [.8 * i for i in action])]

            last_day = list(self.current_prices.index)[-1]
            share_price = []
            # print(self.weights)
            # print(action)
            for i in range(len(self.codes)):
                investment = self.weights[i + 1] * self.money
                share_price.append(
                    (self.current_prices.loc[(self.current_prices['code'] == self.codes[i]), 'adj close']).loc[
                        last_day])

                self.share_count[i + 1] = int(investment / share_price[i])

            self.share_count[0] = self.money - sum(np.multiply(self.share_count[1:], share_price))
            self.weights = [self.share_count[0] / self.money] + [i / self.money for i in
                                                                 np.multiply(self.share_count[1:], share_price)]

            self.total_steps += 1

            if self.total_steps == self.max_steps or self.total_steps == self.training_steps:
                self.done = True
                # self.reset()

            self.current_state, self.current_prices = self.get_next_state(), \
                                                      self.price_history[self.total_steps - 1]

            last_day = list(self.current_prices.index)[-1]
            share_price = []
            for i in range(self.portfolio_size - 1):
                share_price.append(
                    (self.current_prices.loc[(self.current_prices['code'] == self.codes[i]), 'adj close']).loc[
                        last_day])

            self.previous_money = self.money
            self.money = sum(np.multiply(self.share_count[1:], share_price)) + self.share_count[0]
            # reward is scaled based on the starting money.
            reward = (self.money - self.previous_money) * self.reward_scale
            self.total_reward += reward

            if self.money < 0:
                self.done = True
                reward += -10

        info = {'Reward': reward, 'Total Reward': self.total_reward, 'Total Steps': self.total_steps,
                'Current portfolio alocation': self.weights, 'Money': self.money,
                'Current shares owned': self.share_count}

        return self.current_state, reward, self.done, info

    def render(self, mode="human"):
        pass

    def reset(self, training=True):
        self.done = False

        if training:
            self.states = self.tf_train_states
            self.price_history = self.train_price_history
        else:
            self.states = self.tf_test_states
            self.price_history = self.test_price_history

        iter_size = iter(self.states)

        self.max_steps = len(list(iter_size))

        # Start training at a random point.
        self.total_steps = int(np.random.randint(1, self.max_steps * .4, 1))
        self.training_steps = self.total_steps + self.episode_length

        print("Reseted, start_step=", self.total_steps)

        self.money = self.starting_money
        self.total_reward = 0
        self.share_count = list(np.zeros(self.portfolio_size))
        self.weights = np.concatenate(([1], list(np.zeros(len(self.codes)))), axis=None)
        self.iterator = iter(self.states)
        self.iterator = itertools.islice(self.iterator, self.total_steps - 1, None)
        self.current_state, self.current_prices = self.get_next_state(), self.price_history[self.total_steps - 1]
        return self.current_state

    def get_next_state(self):
        next_state = list(next(self.iterator).values())
        next_state = list(next(iter(next_state)))
        return np.asarray(next_state)

    def normalized_sample(self, sample):

        if type(sample) is tf.Tensor:
            sample = sample.numpy()

        # Normalize Samples, such as they always sums to 1.
        sample /= np.sum(sample)
        sample = np.insert(sample, np.random.randint(1, len(sample), 1), np.random.random_sample(1))
        sample[random.sample(range(len(sample)), 2)] = 1, 0
        sample.sort()
        sample = np.array([sample[i + 1] - sample[i] for i in range(len(sample) - 1)])

        return sample

    def normalized_action(self, action):
        total_sum = tf.reduce_sum(action).numpy()
        divisor = [total_sum for _ in range(self.portfolio_size)]
        action = tf.divide(action, divisor).numpy()
        return action

    def get_data(self, is_training=True):
        datasets = dict()

        def scale(state):
            state['adj close'] /= last_close
            state['kama'] /= last_close
            keys = ', '
            keys = keys.join(list(state.keys()))

            new_state = dict()
            new_state[keys] = tf.concat(list(state.values()), axis=0)
            return new_state

        if self.old_dataset:
            if is_training:
                names = ['train', 'test']
                for name in names:
                    filename = os.path.join('gs://data_mauro/' + 'full_data', name + '.tfrecord')
                    datasets[name] = self.load_dataset(filename)
            else:
                filename = os.path.join('gs://data_mauro/' + 'full_data', 'test.tfrecord')
                datasets['test'] = self.load_dataset(filename)

            self.train_price_history = pd.read_csv(
                os.path.join('gs://data_mauro/' + 'full_data', 'train_price_history.csv'),
                index_col=0, parse_dates=True, dtype=object)
            self.test_price_history = pd.read_csv(
                os.path.join('gs://data_mauro/' + 'full_data', 'test_price_history.csv'),
                index_col=0, parse_dates=True, dtype=object)

            # dataset = datasets['train'].map(scale) if is_training else datasets['test'].map(scale)
        else:
            self.data = pd.read_csv('gs://data_mauro/' + self.market + '.csv', index_col=0, parse_dates=True,
                                    dtype=object)

            self.data["code"] = self.data["code"].astype(str)

            data2 = self.data.loc[self.data["code"].isin(self.codes)]
            date_set = set(data2.loc[data2["code"] == self.codes[0]].index)

            for code in self.codes:
                date_set = date_set.intersection((set(data2.loc[data2['code'] == code].index)))

            # The most recent and older dates for the data to be used. Note that the data set will
            # not always contain all the data for this period, but it ensures that only data from this interval is
            # chosen.
            start_date, end_date = "2016-09-14", "2021-09-13"
            date_set = date_set.intersection(set(pd.date_range(start_date, end_date)))
            date_set = list(date_set)
            date_set.sort()

            start_time = date_set[0]
            end_time = date_set[int(len(date_set) / 6) * 5 - 1]
            test_start_time = date_set[int(len(date_set) / 6) * 5]
            test_end_time = date_set[-1]

            self.data[self.features[:-3]] = self.data[self.features[:-3]].astype(float)
            self.data = self.data.sort_index()

            train_data = self.data[start_time.strftime("%Y-%m-%d"):end_time.strftime("%Y-%m-%d")]
            test_data = self.data[test_start_time.strftime("%Y-%m-%d"):test_end_time.strftime("%Y-%m-%d")]

            datasets['train'], self.train_price_history = self.prepare_data(train_data, start_time, end_time)
            datasets['test'], self.test_price_history = self.prepare_data(test_data, test_start_time, test_end_time)

            self.train_price_history.to_csv(os.path.join('gs://data_mauro', 'full_data', 'train_price_history.csv'))
            self.test_price_history.to_csv(os.path.join('gs://data_mauro', 'full_data', 'test_price_history.csv'))

            # print(datasets['test'])
            self.save_tfrecord(datasets['train'], 'train')
            self.save_tfrecord(datasets['test'], 'test')

        # Generating the window using pandas.
        # This is useful here since we want to also store the indexes of the the dataset.
        price_list = []
        for i, window in enumerate(self.train_price_history.rolling(window=self.window_length * 3)):
            if len(window) == (self.window_length * 3):
                if ((i + 1) % 3) == 0:
                    price_list.append(pd.DataFrame(window))
            else:
                pass
        self.train_price_history = price_list

        price_list = []
        for i, window in enumerate(self.test_price_history.rolling(window=self.window_length * 3)):
            if i >= (self.window_length - 1) * 3:
                if ((i + 1) % 3) == 0:
                    price_list.append(pd.DataFrame(window))
            else:
                pass

        self.test_price_history = price_list
        filename = os.path.join('gs://data_mauro/' + 'full_data', 'train.tfrecord')
        self.tf_train_states = self.load_dataset(filename)
        filename = os.path.join('gs://data_mauro/' + 'full_data', 'test.tfrecord')
        self.tf_test_states = self.load_dataset(filename)

        *_, last_prices = iter(self.tf_test_states)
        last_close = last_prices['adj close'].numpy()

        self.tf_test_states = self.tf_test_states.map(scale)
        self.tf_train_states = self.tf_train_states.map(scale)

        # windowing the tf_dataset
        self.tf_train_states = self.tf_train_states.window(self.window_length,
                                                           shift=1,
                                                           drop_remainder=True)
        # self.save_tfrecord(dataset, 'train', windowed=True)
        # self.tf_train_states = self.strategy.distribute_datasets_from_function(lambda _: self.tf_train_states)

        self.tf_test_states = self.tf_test_states.window(self.window_length,
                                                         shift=1,
                                                         drop_remainder=True)
        # self.save_tfrecord(dataset, 'test', windowed=True)
        # self.tf_test_states = self.strategy.distribute_datasets_from_function(lambda _: self.tf_test_states)

    def prepare_data(self, data_set, start_time, end_time):

        date_set = pd.date_range(start_time, end_time)
        # Generate data for each asset
        asset_data = pd.DataFrame()
        data = pd.DataFrame()
        for asset in self.codes:
            current_asset = data_set[data_set["code"] == asset].reindex(date_set)
            current_asset['volume'] = current_asset['volume'].fillna(0)
            current_asset['adj close'] = current_asset['adj close'].fillna(method='ffill')
            current_asset['code'] = current_asset['code'].fillna(method='ffill')
            current_asset = current_asset.fillna(method='ffill', axis=1)
            current_asset = current_asset.fillna(method='bfill', axis=1)

            asset_data['adj close'] = current_asset['adj close']
            asset_data['adj close'] = asset_data['adj close']
            asset_data['rsi'] = momentum.rsi(current_asset['adj close']) / 100
            asset_data['mfi'] = volume.money_flow_index(current_asset['high'].astype(float),
                                                        current_asset['low'].astype(float),
                                                        current_asset['adj close'].astype(float),
                                                        current_asset['volume'].astype(float)) / 100
            asset_data['kama'] = momentum.kama(current_asset['adj close'])
            asset_data['code'] = [str(asset)] * asset_data.shape[0]

            data = data.append(asset_data)
        price_df = data[['adj close', 'code']]
        price_df = price_df.sort_index()
        price_history = price_df[(14 - 1) * 3:]
        gb = data.groupby(data.index)

        result = pd.DataFrame()
        column = self.features + ['code']

        for ft in column:
            result[str(ft)] = gb[str(ft)].unique()

        result = result.drop('code', axis=1)

        result = result.apply(self.verific_space, axis=1, raw=True)

        result = result.iloc[13:]
        states = result

        return states, price_history

    def verific_space(self, state):
        for i, ft in enumerate(state):
            if len(ft) != len(self.codes):
                diff = len(self.codes) - len(ft)
                state[i] = np.insert(ft, np.arange(diff), np.zeros(diff))
        return state

    @staticmethod
    def _float_feature(values):
        """Returns a float_list from a float / double."""
        return tf.train.Feature(float_list=tf.train.FloatList(value=values))

    def serialize_example(self, state, column=None, windowed=False):
        """
            Creates a tf.train.Example message ready to be written to a file.
            If column is None, then windowed needs to be false, since we will be storing the
            "batched" version of the states.
        """
        if windowed:
            feature = dict()
            for i, time_step in enumerate(state):
                string = 'feature{}'.format(str(i).zfill(3))
                feature[string] = self._float_feature(time_step)
            example_proto = tf.train.Example(features=tf.train.Features(feature=feature))
            return example_proto.SerializeToString()
        else:
            feature = dict()
            for k, v in zip(column, state):
                feature[k] = self._float_feature([*v])
            # Create a Features message using tf.train.Example.
            example_proto = tf.train.Example(features=tf.train.Features(feature=feature))
            return example_proto.SerializeToString()

    def parse_tfrecord(self, example_proto, windowed=False):
        # Parse the input `tf.train.Example`.
        descr = self.get_description(windowed)
        example = tf.io.parse_single_example(example_proto, descr)
        return example

    def load_dataset(self, filename):
        records = tf.data.TFRecordDataset(filename)
        return records.map(self.parse_tfrecord)

    def get_description(self, windowed=False):
        num_assets = self.portfolio_size - 1
        if windowed:
            feature_description = dict()
            size = num_assets * len(self.codes)
            for i in range(self.window_length):
                string = 'feature{}'.format(str(i).zfill(3))
                feature_description[string] = tf.io.FixedLenFeature([size], tf.float32)
        else:
            column = self.features
            feature_description = dict()
            for ft in column:
                feature_description[ft] = tf.io.FixedLenFeature([num_assets], tf.float32)
            return feature_description

    def save_tfrecord(self, to_save, train_or_test, windowed=False):
        if windowed:
            # os.makedirs(os.path.join('gs://data_mauro', 'windowed_data', train_or_test), exist_ok=True)
            dirctry = os.path.join('gs://data_mauro', 'windowed_data', train_or_test)
            for mini_batch in to_save:
                filename = train_or_test + str(self.file_save_counter) + ".tfrecord"
                # print(os.path.join(folder, filename).encode('Latin-1'))
                with tf.io.TFRecordWriter(os.path.join(dirctry, filename)) as out_file:
                    tf_record = self.serialize_example(mini_batch, windowed=True)
                    out_file.write(tf_record)
                self.file_save_counter += 1
            self.file_save_counter = 1
        else:
            column = self.features
            # os.makedirs('gs://data_mauro/' + 'full_data', exist_ok=True)
            dirctry = 'gs://data_mauro/' + 'full_data'
            filename = os.path.join(dirctry, train_or_test + '.tfrecord')
            with tf.io.TFRecordWriter(filename) as out_file:
                for line in to_save.itertuples(index=False):
                    tf_record = self.serialize_example(line, column)
                    out_file.write(tf_record)

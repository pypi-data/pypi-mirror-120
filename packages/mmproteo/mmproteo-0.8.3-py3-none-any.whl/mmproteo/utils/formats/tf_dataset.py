import gc
import os
import shutil
import time
from typing import List, Dict, Union, Callable, Any, Optional, Iterable, Tuple

import numpy as np
import pandas as pd
import tensorflow as tf
import tensorflow_datasets as tfds

from mmproteo.utils import log, utils
from mmproteo.utils.processing import ItemProcessor


class Parquet2DatasetFileProcessor:

    def __init__(self,
                 training_data_columns: List[str],
                 target_data_columns: List[str],
                 padding_lengths: Dict[str, int],
                 padding_characters: Dict[str, Union[str, int, float]],
                 column_normalizations: Dict[str, Callable[[Any], Any]],
                 dataset_dump_path_prefix: str,
                 char_to_idx_mappers: Optional[Dict[str, Dict[str, int]]] = None,
                 char_to_idx_mapping_functions: Optional[Dict[str, Callable[[str], int]]] = None,
                 item_count: int = 0,
                 skip_existing: bool = True,
                 split_on_column_values_of: Optional[List[str]] = None,
                 logger: log.Logger = log.DEFAULT_LOGGER
                 ):
        self.training_data_columns = training_data_columns
        self.target_data_columns = target_data_columns
        self.padding_lengths = padding_lengths
        self.padding_characters = padding_characters
        self.column_normalizations = column_normalizations
        self.char_to_idx_mapping_functions = char_to_idx_mapping_functions
        if self.char_to_idx_mapping_functions is None:
            assert char_to_idx_mappers is not None, \
                "either char_to_idx_mappers or char_to_idx_mapping_functions must be given"
            self.char_to_idx_mapping_functions = {
                column: mapping.get for column, mapping in char_to_idx_mappers.items()  # type: ignore
            }
        self.item_count = item_count
        self.dataset_dump_path_prefix = dataset_dump_path_prefix
        self.char_idx_dtype = np.int8
        self.skip_existing = skip_existing
        self.split_on_column_values_of = split_on_column_values_of
        self.logger = logger

    def normalize_columns(self, df: pd.DataFrame, df_name: str = "?") -> pd.DataFrame:
        if self.column_normalizations is None:
            return df
        df = df.copy()
        for column, normalize_func in self.column_normalizations.items():
            df[column] = df[column].apply(normalize_func)
        self.logger.debug(f"normalized df '{df_name}'")
        return df

    def pad_array_columns(self, df: pd.DataFrame, df_name: str = "?") -> pd.DataFrame:
        if len(df) == 0:
            return df

        df = df.copy()
        for column, padding_length in self.padding_lengths.items():
            item_dtype = df[column].iloc[0].dtype

            df[column] = list(tf.keras.preprocessing.sequence.pad_sequences(
                sequences=df[column],
                maxlen=padding_length,
                padding='post',
                value=self.padding_characters[column],
                dtype=item_dtype
            ))
        self.logger.debug(f"padded df '{df_name}'")
        return df

    @staticmethod
    def _sequence_to_indices(sequence: Iterable[str],
                             char_to_idx_mapping_func: Callable[[str], int],
                             dtype: type) -> np.ndarray:
        return np.array([char_to_idx_mapping_func(char) for char in sequence],
                        dtype=dtype)

    def sequence_column_to_indices(self, df: pd.DataFrame, df_name: str = "?") -> pd.DataFrame:
        assert self.char_to_idx_mapping_functions is not None, \
            "the char_to_idx mapping functions should have been initialized"
        if len(self.char_to_idx_mapping_functions) == 0:
            return df
        df = df.copy()
        for column, mapping_function in self.char_to_idx_mapping_functions.items():
            df[column] = df[column].apply(lambda seq: self._sequence_to_indices(seq,
                                                                                mapping_function,
                                                                                self.char_idx_dtype))
        self.logger.debug(f"mapped sequences to indices for '{df_name}'")
        return df

    @staticmethod
    def stack_numpy_arrays_in_dataframe(df: pd.DataFrame) -> pd.DataFrame:
        return df.apply(lambda item: [np.stack(item)])

    def preprocess_dataframe(self, df: pd.DataFrame, df_name: str = "?") -> pd.DataFrame:
        """

        :param df_name:
        :param df:
        :return: a stacked dataframe (with one single row)
        """
        df = self.normalize_columns(df, df_name=df_name)
        df = self.pad_array_columns(df, df_name=df_name)
        df = self.sequence_column_to_indices(df, df_name=df_name)
        df = self.stack_numpy_arrays_in_dataframe(df)
        self.logger.debug(f"finished preprocessing df '{df_name}'")
        return df

    def stacked_df_to_dataset(self, stacked_df: pd.DataFrame, df_name: str = "?") -> tf.data.Dataset:
        assert len(stacked_df) == 1, "all column values should be stacked at this point"
        training_data = tuple(stacked_df[self.training_data_columns].iloc[0])
        target_data = tuple(stacked_df[self.target_data_columns].iloc[0])
        tf_dataset = tf.data.Dataset.from_tensor_slices((training_data, target_data))
        self.logger.debug(f"created TF dataset from stacked df '{df_name}'")
        return tf_dataset

    def split_dataframe_by_column_values(self,
                                         df: pd.DataFrame,
                                         tf_dataset_output_file_path: str) -> List[Tuple[str, pd.DataFrame]]:
        if self.split_on_column_values_of is None or len(self.split_on_column_values_of) == 0:
            self.logger.debug(f"skipped splitting df for '{tf_dataset_output_file_path}' by column values")
            return [(tf_dataset_output_file_path, df)]
        if len(self.split_on_column_values_of) == 1:
            value_groups = [((values,), df_split) for values, df_split in df.groupby(self.split_on_column_values_of)]
        else:
            value_groups = [(values, df_split) for values, df_split in df.groupby(self.split_on_column_values_of)]
        results = [(
            os.path.join(
                tf_dataset_output_file_path,
                *[str(value).replace("/", "_") for value in values]),
            df_split.drop(columns=self.split_on_column_values_of)
        ) for values, df_split in value_groups]

        self.logger.debug(f"finished splitting df for '{tf_dataset_output_file_path}' by column values")

        return results

    def convert_df_file_to_dataset_file(self,
                                        df_input_file_path: str,
                                        tf_dataset_output_file_path: str) -> Optional[Tuple[tf.TensorSpec]]:
        df = pd.read_parquet(df_input_file_path)
        self.logger.debug(f"finished reading '{df_input_file_path}' file")
        df_splits = self.split_dataframe_by_column_values(df, tf_dataset_output_file_path)
        if len(df_splits) == 0:
            return None

        self.logger.debug(f"storing {len(df_splits)} df split{utils.get_plural_s(len(df_splits))} "
                          f"from '{df_input_file_path}'")
        tf_dataset = None

        for path, df_split in df_splits:
            preprocessed_df = self.preprocess_dataframe(df_split, df_name=path)
            tf_dataset = self.stacked_df_to_dataset(preprocessed_df, df_name=path)
            tf.data.experimental.save(dataset=tf_dataset,
                                      path=path,
                                      compression='GZIP')
            self.logger.debug(f"saved TF dataset to {path}")
        assert tf_dataset is not None, "at least one df_split should have created a dataset"

        self.logger.debug(f"TF dataset element spec: {tf_dataset.element_spec}")
        return tf_dataset.element_spec

    def __call__(self, item: Tuple[int, str]) -> Optional[Dict[str, Optional[Any]]]:
        idx, path = item
        tf_dataset_path = os.path.join(self.dataset_dump_path_prefix, path.split(os.path.sep)[-1])

        info_text = f"item {idx + 1}/{self.item_count}: '{path}'"
        start_info_text = "Preprocessing " + info_text
        stop_info_text = "Finished preprocessing " + info_text
        if idx % 10 == 0:
            self.logger.info(start_info_text)
        else:
            self.logger.debug(start_info_text)

        if self.skip_existing and os.path.exists(tf_dataset_path):
            self.logger.debug(f"Skipped '{path}' because '{tf_dataset_path}' already exists")
            return None

        element_spec = self.convert_df_file_to_dataset_file(df_input_file_path=path,
                                                            tf_dataset_output_file_path=tf_dataset_path)
        gc.collect()
        if idx % 10 == 0:
            self.logger.info(stop_info_text)
        else:
            self.logger.debug(stop_info_text)

        res = {
            'dataset_path': tf_dataset_path,
            'element_spec': element_spec,
        }
        return res

    def process(self, parquet_file_paths: Iterable[str], **kwargs: Any) -> List[Optional[Dict[str, Optional[Any]]]]:
        if len(tf.config.list_physical_devices(device_type="GPU")) > 0:
            self.logger.info("Tensorflow dataset creation performance can be increased by limiting TF to CPUs only. "
                             'Set the following environment variables: "CUDA_DEVICE_ORDER"="PCI_BUS_ID" and '
                             '"CUDA_VISIBLE_DEVICES"="-1"')
        item_processor = ItemProcessor(
            items=enumerate(parquet_file_paths),
            item_processor=self.__call__,
            action_name="parquet2tf_dataset-process",
            subject_name="mzmlid parquet file",
            logger=self.logger,
            **kwargs
        )
        results: List[Optional[Dict[str, Optional[Any]]]] = list(item_processor.process())  # type: ignore
        return results


class DatasetLoader:
    def __init__(
            self,
            element_spec: Iterable[Union[Iterable[tf.TensorSpec], tf.TensorSpec]],
            batch_size: Optional[int] = 32,
            drop_batch_remainder: bool = True,
            shuffle_buffer_size: Optional[int] = 200_000,
            reshuffle_each_iteration: bool = True,
            prefetch_mode: Optional[int] = tf.data.experimental.AUTOTUNE,
            run_benchmarks: bool = False,
            deterministic: Optional[bool] = False,
            thread_count: Optional[int] = os.cpu_count(),
            cache_path: Optional[str] = None,
            keep_cache: bool = True,
            options: Optional[tf.data.Options] = None,
            logger: log.Logger = log.DEFAULT_LOGGER,
    ):
        self.element_spec = element_spec
        self.batch_size = batch_size
        self.drop_batch_remainder = drop_batch_remainder
        self.shuffle_buffer_size = shuffle_buffer_size
        self.reshuffle_each_iteration = reshuffle_each_iteration
        self.prefetch_mode = prefetch_mode
        self.run_benchmarks = run_benchmarks
        self.deterministic = deterministic
        if thread_count is None:
            thread_count = 1
        self.thread_count = thread_count
        self.cache_path = cache_path
        self.keep_cache = keep_cache
        self.options = options
        self.logger = logger

    def _apply_options(self, dataset: tf.data.Dataset, name: str = "unknown") -> tf.data.Dataset:
        if self.options is None:
            self.logger.debug(f"skipped applying options to dataset '{name}'")
            return dataset
        ds = dataset.with_options(options=self.options)
        self.logger.debug(f"applied options to dataset '{name}'")
        return ds

    def _load_dataset_from_file(self, path: str) -> tf.data.Dataset:
        return tf.data.experimental.load(
                path=path,
                element_spec=self.element_spec,
                compression='GZIP'
            )

    def _load_dataset_interleaved(self, paths: List[str], name: str = "unknown") -> tf.data.Dataset:
        ds = tf.data.Dataset.from_tensor_slices(paths)
        ds = self._apply_options(dataset=ds, name=name)
        ds = ds.interleave(
            map_func=self._load_dataset_from_file,
            num_parallel_calls=self.thread_count,
            deterministic=self.deterministic,
        )
        self.logger.debug(f"loaded dataset '{name}' interleaved")
        return ds

    def _shuffle_dataset(self, dataset: tf.data.Dataset, name: str = "unknown") -> tf.data.Dataset:
        if self.shuffle_buffer_size is None:
            self.logger.debug(f"skipped shuffling dataset '{name}'")
            return dataset
        ds = dataset.shuffle(
            buffer_size=self.shuffle_buffer_size,
            reshuffle_each_iteration=self.reshuffle_each_iteration
        )
        self.logger.debug(f"shuffled dataset '{name}'")
        return ds

    def _batch_dataset(self, dataset: tf.data.Dataset, name: str = 'unknown') -> tf.data.Dataset:
        if self.batch_size is None:
            self.logger.debug(f"skipped batching dataset '{name}'")
            return dataset
        ds = dataset.batch(
            batch_size=self.batch_size,
            drop_remainder=self.drop_batch_remainder,
            # deterministic=self.deterministic,  # introduced in TF 2.5.0
            # num_parallel_calls=self.thread_count,  # introduced in TF 2.5.0
        )
        self.logger.debug(f"batched dataset '{name}'")
        return ds

    def _cache_dataset(self, dataset: tf.data.Dataset, name: str = "unknown") -> tf.data.Dataset:
        if self.cache_path is None:
            self.logger.debug(f"skipped caching dataset '{name}'")
            return dataset

        try:
            if not self.keep_cache:
                shutil.rmtree(self.cache_path)
                self.logger.debug(f"removed previous cache at '{self.cache_path}'")
        except FileNotFoundError:
            pass

        utils.ensure_dir_exists(self.cache_path)
        ds = dataset.cache(os.path.join(self.cache_path, name))
        self.logger.debug(f"cached dataset '{name}'")
        return ds

    def _prefetch_dataset(self, dataset: tf.data.Dataset, name: str = 'unknown') -> tf.data.Dataset:
        if self.prefetch_mode is None:
            self.logger.debug(f"skipped configuring prefetching for dataset '{name}'")
            return dataset
        ds = dataset.prefetch(
            buffer_size=self.prefetch_mode
        )
        self.logger.debug(f"configured prefetching for dataset '{name}'")
        return ds

    def _run_benchmark(self, dataset: tf.data.Dataset, name: str = 'unknown') -> None:
        if self.run_benchmarks:
            self.logger.info(f"running benchmark for '{name}' dataset")
            tfds.benchmark(dataset)
            gc.collect()
            self.logger.info(f"ran benchmark for '{name}' dataset - waiting 5 seconds")
            time.sleep(5)
        else:
            self.logger.debug(f"skipped benchmarking dataset '{name}'")

    def prepare_dataset(self, paths: Union[str, List[str]], name: str = 'my_dataset') -> tf.data.Dataset:
        self.logger.debug(f"preparing dataset '{name}' with {len(paths)} paths")
        if isinstance(paths, str):
            path_list: List[str] = [paths]
        else:
            path_list = paths
        dataset = self._load_dataset_interleaved(paths=path_list, name=name)
        dataset = self._shuffle_dataset(dataset, name=name)
        dataset = self._batch_dataset(dataset, name=name)
        dataset = self._cache_dataset(dataset, name=name)
        dataset = self._prefetch_dataset(dataset, name=name)
        self._run_benchmark(dataset, name=name)
        self.logger.info(f"prepared dataset '{name}'")
        return dataset

    def load_datasets_by_type(self, dataset_file_paths: Dict[str, List[str]]) -> Dict[str, tf.data.Dataset]:
        datasets = {
            training_data_type: self.prepare_dataset(paths, name=training_data_type)
            for training_data_type, paths in dataset_file_paths.items()
        }
        return datasets

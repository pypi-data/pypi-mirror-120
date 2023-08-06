#!/usr/bin/env python3

"""Module containing the InterBasePairCorrelation class and the command line interface."""
import argparse
from itertools import product

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

from biobb_common.configuration import settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_dna.utils.loader import read_series
from biobb_dna.utils import constants


class InterBasePairCorrelation():
    """
    | biobb_dna InterBasePairCorrelation
    | Calculate correlation between all base pairs of a single sequence and for a single helical parameter.

    Args:
        input_filename_shift (str): Path to .ser file with data for helical parameter 'shift'. File type: input. Accepted formats: ser (edam:format_2330).
        input_filename_slide (str): Path to .ser file with data for helical parameter 'slide'. File type: input. Accepted formats: ser (edam:format_2330).
        input_filename_rise (str): Path to .ser file with data for helical parameter 'rise'. File type: input. Accepted formats: ser (edam:format_2330).
        input_filename_tilt (str): Path to .ser file with data for helical parameter 'tilt'. File type: input. Accepted formats: ser (edam:format_2330).
        input_filename_roll (str): Path to .ser file with data for helical parameter 'roll'. File type: input. Accepted formats: ser (edam:format_2330).
        input_filename_twist (str): Path to .ser file with data for helical parameter 'twist'. File type: input. Accepted formats: ser (edam:format_2330).
        output_csv_path (str): Path to directory where output is saved. File type: output. Accepted formats: csv (edam:format_3752).
        output_jpg_path (str): Path to .jpg file where output is saved. File type: output. Accepted formats: jpg (edam:format_3579).
        properties (dict):
            * **sequence** (*str*) - (None) Nucleic acid sequence for the input .ser file. Length of sequence is expected to be the same as the total number of columns in the .ser file, minus the index column (even if later on a subset of columns is selected with the *seqpos* option).
            * **seqpos** (*list*) - (None) list of sequence positions (columns indices starting by 0) to analyze.  If not specified it will analyse the complete sequence.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_dna.interbp_correlations.interbpcorr import interbasepaircorrelation

            interbasepaircorrelation(
                input_filename_shift='path/to/input/shift.ser',
                input_filename_slide='path/to/input/slide.ser',
                input_filename_rise='path/to/input/slide.ser',
                input_filename_tilt='path/to/input/tilt.ser',
                input_filename_roll='path/to/input/roll.ser',
                input_filename_twist='path/to/input/twist.ser',
                output_csv_path='path/to/output/file.csv',
                output_jpg_path='path/to/output/plot.jpg',
                properties=prop)
    Info:
        * wrapped_software:
            * name: In house
            * license: Apache-2.0
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl

    """

    def __init__(
            self, input_filename_shift, input_filename_slide,
            input_filename_rise, input_filename_tilt,
            input_filename_roll, input_filename_twist,
            output_csv_path, output_jpg_path,
            properties=None, **kwargs) -> None:
        properties = properties or {}

        # Input/Output files
        self.io_dict = {
            'in': {
                'input_filename_shift': input_filename_shift,
                'input_filename_slide': input_filename_slide,
                'input_filename_rise': input_filename_rise,
                'input_filename_tilt': input_filename_tilt,
                'input_filename_roll': input_filename_roll,
                'input_filename_twist': input_filename_twist
            },
            'out': {
                'output_csv_path': output_csv_path,
                'output_jpg_path': output_jpg_path
            }
        }

        self.properties = properties
        self.sequence = properties.get("sequence", None)
        self.seqpos = properties.get("seqpos", None)

        # Properties common in all BB
        self.can_write_console_log = properties.get(
            'can_write_console_log', True)
        self.global_log = properties.get('global_log', None)
        self.prefix = properties.get('prefix', None)
        self.step = properties.get('step', None)
        self.path = properties.get('path', '')
        self.remove_tmp = properties.get('remove_tmp', True)
        self.restart = properties.get('restart', False)

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`HelParCorrelation <correlations.interbpcorr.InterBasePairCorrelation>` object."""

        # Get local loggers from launchlogger decorator
        out_log = getattr(self, 'out_log', None)
        err_log = getattr(self, 'err_log', None)

        # Check the properties
        fu.check_properties(self, self.properties)

        # check sequence
        if self.sequence is None or len(self.sequence) < 2:
            raise ValueError("sequence is null or too short!")

        # check seqpos
        if self.seqpos is not None:
            if not (isinstance(self.seqpos, list) and len(self.seqpos) > 1):
                raise ValueError(
                    "seqpos must be a list of at least two integers")

        # Restart
        if self.restart:
            output_file_list = [
                self.io_dict['out']['output_csv_path'],
                self.io_dict['out']['output_jpg_path']]
            if fu.check_complete_files(output_file_list):
                fu.log('Restart is enabled, this step: %s will the skipped' %
                       self.step, out_log, self.global_log)
                return 0

        # Creating temporary folder
        self.tmp_folder = fu.create_unique_dir(prefix="bpcorrelation_")
        fu.log('Creating %s temporary folder' % self.tmp_folder, out_log)

        # read input
        shift = read_series(
            self.io_dict["in"]["input_filename_shift"], usecols=self.seqpos)
        slide = read_series(
            self.io_dict["in"]["input_filename_slide"], usecols=self.seqpos)
        rise = read_series(
            self.io_dict["in"]["input_filename_rise"], usecols=self.seqpos)
        tilt = read_series(
            self.io_dict["in"]["input_filename_tilt"], usecols=self.seqpos)
        roll = read_series(
            self.io_dict["in"]["input_filename_roll"], usecols=self.seqpos)
        twist = read_series(
            self.io_dict["in"]["input_filename_twist"], usecols=self.seqpos)

        if self.seqpos is None:
            # drop first and last columns
            shift = shift[shift.columns[1:-2]]
            slide = slide[slide.columns[1:-2]]
            rise = rise[rise.columns[1:-2]]
            tilt = tilt[tilt.columns[1:-2]]
            roll = roll[roll.columns[1:-2]]
            twist = twist[twist.columns[1:-2]]
            labels = [
                f"{self.sequence[i:i+2]}" for i in range(1, len(shift.columns) + 1)]
            corr_index = [
                f"{self.sequence[i:i+3]}" for i in range(1, len(shift.columns) + 1)]
        else:
            labels = [f"{self.sequence[i:i+2]}" for i in self.seqpos]
            corr_index = [f"{self.sequence[i:i+3]}" for i in self.seqpos]

        # rename duplicated subunits
        shift.columns = labels
        while any(shift.columns.duplicated()):
            shift.columns = [
                name if not duplicated else name + "_dup"
                for duplicated, name
                in zip(shift.columns.duplicated(), shift.columns)]
        unique_labels = shift.columns
        slide.columns = unique_labels
        rise.columns = unique_labels
        tilt.columns = unique_labels
        roll.columns = unique_labels
        twist.columns = unique_labels

        # set names to each dataset
        shift.name = "shift"
        slide.name = "slide"
        rise.name = "rise"
        tilt.name = "tilt"
        roll.name = "roll"
        twist.name = "twist"

        # get correlation between neighboring basepairs among all helical parameters
        results = {}
        datasets = [shift, slide, rise, tilt, roll, twist]
        for ser1, ser2 in product(datasets, datasets):
            ser2_shifted = ser2.shift(axis=1)
            ser2_shifted[unique_labels[0]] = ser2[unique_labels[-1]]
            if (
                    ser1.name in constants.hp_angular and
                    ser2.name in constants.hp_angular):
                method = self.circular
            elif (
                (
                    ser1.name in constants.hp_angular and not (
                        ser2.name in constants.hp_angular)
                ) or (
                    ser2.name in constants.hp_angular and not (
                        ser1.name in constants.hp_angular)
                )
            ):
                method = self.circlineal
            else:
                method = "pearson"
            corr_data = ser1.corrwith(ser2_shifted, method=method)
            corr_data.index = corr_index
            results[f"{ser1.name}/{ser2.name}"] = corr_data
        result_df = pd.DataFrame.from_dict(results)
        result_df.index = corr_index

        # save csv data
        result_df.to_csv(self.io_dict["out"]["output_csv_path"])

        # create heatmap
        cmap = plt.get_cmap("bwr")
        bounds = [-1, -.8, -.6, -.4, -.2, .2, .4, .6, .8, 1]
        num = cmap.N
        norm = mpl.colors.BoundaryNorm(bounds, num)
        cmap.set_bad(color="gainsboro")
        fig, ax = plt.subplots(
            1,
            1,
            dpi=300,
            figsize=(7.5, 5),
            tight_layout=True)
        im = ax.imshow(result_df, cmap=cmap, norm=norm, aspect='auto')
        plt.colorbar(im, ticks=[-1, -.8, -.6, -.4, -.2, .2, .4, .6, .8, 1])

        # axes
        xlocs = np.arange(len(result_df.columns))
        _ = ax.set_xticks(xlocs)
        _ = ax.set_xticklabels(result_df.columns.to_list(), rotation=90)

        ylocs = np.arange(len(result_df.index))
        _ = ax.set_yticks(ylocs)
        _ = ax.set_yticklabels(result_df.index.to_list())

        ax.set_title(
            "Correlation for neighboring basepairs "
            "and pairs of helical parameters")

        fig.tight_layout()
        fig.savefig(
            self.io_dict['out']['output_jpg_path'],
            format="jpg")
        plt.close()

        # Remove temporary file(s)
        if self.remove_tmp:
            fu.rm(self.tmp_folder)
            fu.log('Removed: %s' % str(self.tmp_folder), out_log)

        return 0

    @staticmethod
    def circular(x1, x2):
        x1 = x1 * np.pi / 180
        x2 = x2 * np.pi / 180
        diff_1 = np.sin(x1 - x1.mean())
        diff_2 = np.sin(x2 - x2.mean())
        num = (diff_1 * diff_2).sum()
        den = np.sqrt((diff_1 ** 2).sum() * (diff_2 ** 2).sum())
        return num / den

    @staticmethod
    def circlineal(x1, x2):
        x2 = x2 * np.pi / 180
        rc = np.corrcoef(x1, np.cos(x2))[1, 0]
        rs = np.corrcoef(x1, np.sin(x2))[1, 0]
        rcs = np.corrcoef(np.sin(x2), np.cos(x2))[1, 0]
        num = (rc ** 2) + (rs ** 2) - 2 * rc * rs * rcs
        den = 1 - (rcs ** 2)
        correlation = np.sqrt(num / den)
        if np.corrcoef(x1, x2)[1, 0] < 0:
            correlation *= -1
        return correlation


def interbasepaircorrelation(
        input_filename_shift: str, input_filename_slide: str,
        input_filename_rise: str, input_filename_tilt: str,
        input_filename_roll: str, input_filename_twist: str,
        output_csv_path: str, output_jpg_path: str,
        properties: dict = None, **kwargs) -> int:
    """Create :class:`HelParCorrelation <correlations.interbpcorr.InterBasePairCorrelation>` class and
    execute the :meth:`launch() <correlations.interbpcorr.InterBasePairCorrelation.launch>` method."""

    return InterBasePairCorrelation(
        input_filename_shift=input_filename_shift,
        input_filename_slide=input_filename_slide,
        input_filename_rise=input_filename_rise,
        input_filename_tilt=input_filename_tilt,
        input_filename_roll=input_filename_roll,
        input_filename_twist=input_filename_twist,
        output_csv_path=output_csv_path,
        output_jpg_path=output_jpg_path,
        properties=properties, **kwargs).launch()


def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(description='Load .ser file from Canal output and calculate correlation between base pairs of the corresponding sequence.',
                                     formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')

    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_filename_shift', required=True,
                               help='Path to ser file for helical parameter shift. Accepted formats: ser.')
    required_args.add_argument('--input_filename_slide', required=True,
                               help='Path to ser file for helical parameter slide. Accepted formats: ser.')
    required_args.add_argument('--input_filename_rise', required=True,
                               help='Path to ser file for helical parameter rise. Accepted formats: ser.')
    required_args.add_argument('--input_filename_tilt', required=True,
                               help='Path to ser file for helical parameter tilt. Accepted formats: ser.')
    required_args.add_argument('--input_filename_roll', required=True,
                               help='Path to ser file for helical parameter roll. Accepted formats: ser.')
    required_args.add_argument('--input_filename_twist', required=True,
                               help='Path to ser file for helical parameter twist. Accepted formats: ser.')
    required_args.add_argument('--output_csv_path', required=True,
                               help='Path to output file. Accepted formats: csv.')
    required_args.add_argument('--output_jpg_path', required=True,
                               help='Path to output plot. Accepted formats: jpg.')

    args = parser.parse_args()
    args.config = args.config or "{}"
    properties = settings.ConfReader(config=args.config).get_prop_dic()

    interbasepaircorrelation(
        input_filename_shift=args.input_filename_shift,
        input_filename_slide=args.input_filename_slide,
        input_filename_rise=args.input_filename_rise,
        input_filename_tilt=args.input_filename_tilt,
        input_filename_roll=args.input_filename_roll,
        input_filename_twist=args.input_filename_twist,
        output_csv_path=args.output_csv_path,
        output_jpg_path=args.output_jpg_path,
        properties=properties)


if __name__ == '__main__':
    main()

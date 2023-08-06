#!/usr/bin/env python3
"""
bin/elastic-blast.py - See DESC constant below

Author: Christiam Camacho (camacho@ncbi.nlm.nih.gov)
Created: Wed 22 Apr 2020 06:31:30 AM EDT
"""
import os
import sys
import signal
import argparse
import logging
from typing import List
from elb import VERSION
from elb.commands.submit import submit as elb_submit
from elb.commands.status import create_arg_parser as create_status_arg_parser
from elb.commands.delete import delete as elb_delete
from elb.commands.run_summary import create_arg_parser as create_run_summary_arg_parser
from elb.util import check_positive_int, config_logging, UserReportError, SafeExecError
from elb.util import ElbSupportedPrograms, clean_up
from elb import constants
from elb.gcp import check_prerequisites
from elb.config import configure
from elb.elb_config import ElasticBlastConfig


DFLT_LOGFILE = 'elastic-blast.log'
DESC = r"""This application facilitates running BLAST on large amounts of query sequence data
on the cloud"""

# error message for missing Elastic-BLAST task on the command line
NO_TASK_MSG =\
"""Elastic-BLAST task was not specified. Please, use submit, status, delete, or run-summary.
usage: elastic-blast [-h] [--version] {submit,status,delete,run-summary} --cfg <config file> [options]"""

def main():
    """Local main entry point which sets up arguments, undo stack,
    and processes exceptions """
    try:
        signal.signal(signal.SIGINT, signal.default_int_handler)
        clean_up_stack = []
        # Check parameters for Unicode letters and reject if codes higher than 255 occur
        reject_cli_args_with_unicode(sys.argv[1:])
        parser = create_arg_parser()
        args = parser.parse_args()
        if not args.subcommand:
            # report missing command line task
            raise UserReportError(returncode=constants.INPUT_ERROR,
                                  message=NO_TASK_MSG)
        config_logging(args)
        cfg = configure(args)
        logging.info(f"ElasticBLAST {args.subcommand} {VERSION}")
        logging.debug({s: dict(cfg[s]) for s in cfg.sections()})
        check_prerequisites(ElasticBlastConfig(cfg))
        #TODO: use cfg only when args.wait, args.sync, and args.run_label are replicated in cfg
        return args.func(args, cfg, clean_up_stack)
    except (SafeExecError, UserReportError) as e:
        logging.error(e.message)
        # SafeExecError return code is the exit code from command line
        # application ran via subprocess
        if isinstance(e, SafeExecError):
            return constants.DEPENDENCY_ERROR
        return e.returncode
    except KeyboardInterrupt:
        return constants.INTERRUPT_ERROR
    #TODO: process filehelper.TarReadError here
    finally:
        messages = clean_up(clean_up_stack)
        if messages:
            for msg in messages:
                logging.error(msg)
            sys.exit(constants.UNKNOWN_ERROR)


def reject_string_with_unicode(content: str) -> None:
    for c in content:
        if ord(c) > 255:
            raise UserReportError(returncode=constants.INPUT_ERROR,
                                  message=f"Command line has Unicode letters in argument '{content}', can't be processed")


def reject_cli_args_with_unicode(args: List[str]) -> None:
        for arg in args:
            reject_string_with_unicode(arg)


def file_must_exist(path: str) -> str:
    """Check if given  path exists and is a file, helper function for
    argparse.ArgumentParser. If used for a command line argument, the
    application will exit with an error if file is not found or path is not a
    file."""
    if os.path.isfile(path):
        return path
    raise argparse.ArgumentTypeError(f'File {path} was not found')


def positive_int(arg: str) -> int:
    """Positive integer type for argparse.ArgumentParser. Raises
    argparse.ArgumentTypeError if the supplied string is not a positive integer."""
    retval = None
    try:
        retval = check_positive_int(arg)
    except Exception as err:
        raise argparse.ArgumentTypeError(str(err))
    return retval


def create_arg_parser():
    """ Create the command line options parser object for this script. """
    prog = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    parser = ElbArgumentParser(prog=prog, description=DESC,
        epilog="To get help about specific command run %(prog)s command --help")
    parser.add_argument('--version', action='version', version='%(prog)s ' + VERSION)

    common_opts_parser = ElbArgumentParser(add_help=False)
    common_opts_parser.add_argument("--cfg", metavar="FILE",
                                    type=file_must_exist,
                                    help="ElasticBLAST configuration file")
    common_opts_parser.add_argument(f"--{constants.CFG_BLAST_RESULTS}", type=str,
                        help="Bucket URI where to save the output from ElasticBLAST")
    common_opts_parser.add_argument("--logfile", default=DFLT_LOGFILE, type=str,
                                    help="Default: " + DFLT_LOGFILE)
    common_opts_parser.add_argument("--loglevel", default='INFO',
                                    choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
    common_opts_parser.add_argument("--dry-run", action='store_true', 
                                    help="Do not perform any actions")

    sp = parser.add_subparsers(dest='subcommand')#title='Subcommands')
    create_submit_arg_parser(sp, common_opts_parser)
    create_status_arg_parser(sp, common_opts_parser)
    create_delete_arg_parser(sp, common_opts_parser)
    create_run_summary_arg_parser(sp, common_opts_parser)
    return parser


def create_submit_arg_parser(subparser, common_opts_parser):
    """ Create the command line options subparser for the submit command. """
    parser = subparser.add_parser('submit', help='Submit an ElasticBLAST search',
                                  parents=[common_opts_parser])
    parser.add_argument("--program", type=str, help="BLAST program to run",
                        choices=ElbSupportedPrograms().get())
    parser.add_argument("--query", type=str,
                        help="Query sequence data, can be provided as a local path or GCS bucket URI to a single file/tarball")
    parser.add_argument("--db", type=str, help="BLAST database to search")
    parser.add_argument("--num-nodes", type=positive_int,
                        help="Number of worker nodes to use")
    #parser.add_argument("--sync", action='store_true', 
    #                    help="Run in synchronous mode")
    # FIXME: EB-132
    parser.add_argument("--run-label", type=str,
                        help="Run-label to tag this ElasticBLAST search, format: key:value")
    parser.add_argument('blast_opts', nargs=argparse.REMAINDER,
                        metavar='BLAST_OPTS',
                        help="Options to pass to BLAST program")
    parser.set_defaults(func=elb_submit)
    return parser


def create_delete_arg_parser(subparser, common_opts_parser):
    """ Create the command line options subparser for the status command. """
    parser = subparser.add_parser('delete',
                                  parents=[common_opts_parser],
                                  help='Delete resources associated with an ElasticBLAST search')
    # FIXME: EB-132
    parser.add_argument("--run-label", type=str,
                        help="Run-label for the ElasticBLAST search to delete, format: key:value")
    parser.set_defaults(func=elb_delete)


class ElbArgumentParser(argparse.ArgumentParser):
    """Custom argument parser to override application exit code"""
    def exit(self, status=0, message=None):
        """Custom exit function that overrides ArgumentParser application
        exit code"""
        if status:
            super().exit(constants.INPUT_ERROR, message)
        else:
            super().exit()

    def error(self, message):
        """Custom error message that does not print usage on errors"""
        self.exit(constants.INPUT_ERROR, f'{self.prog}: error: {message}\n')


if __name__ == "__main__":
    sys.exit(main())
    import traceback
    try:
        sys.exit(main())
    except Exception as e:
        traceback.print_exc(file=sys.stderr)
        sys.exit(constants.UNKNOWN_ERROR)

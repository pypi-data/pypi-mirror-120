import argparse
import logging

from smalldoc import parse, write

logger = logging.getLogger(__name__)


def get_parameters():
    arg_parser = argparse.ArgumentParser(
        prog='smalldoc',
        description="Generate a human readable documentation of your Python module."
    )
    arg_parser.add_argument(
        "--workspace",
        "-w",
        help="Directory where is placed your module",
        type=str,
        required=True
    )
    arg_parser.add_argument(
        "--module",
        "-m",
        help="The name of your module",
        type=str,
        required=True
    )
    arg_parser.add_argument(
        "--output-file",
        "-o",
        help="Name of file where to write the result documentation",
        type=str,
        required=True
    )
    arg_parser.add_argument(
        "--log",
        "-l",
        help="Log level",
        type=str
    )

    return vars(arg_parser.parse_args())


def param_missing(param_name, input_params):
    logger.debug('test if miss params %s', param_name)
    if param_name not in input_params or input_params[param_name] == '' or input_params[param_name] is None:
        logger.error('missing params --%s', param_name)
        return True
    return False


def main():
    logger.debug("Parsing parameters")
    params = get_parameters()
    if params['log'] != "":
        logging.basicConfig(level=params['log'])
    logger.debug("Parameters loaded")
    if params['log'] == "DEBUG":
        for k, v in params.items():
            if k != "password":
                logger.debug("%s: %s", k, v)

    if param_missing('workspace', params) or param_missing('module', params) or param_missing('output_file', params):
        exit(1)

    parse_result = parse(
        params['workspace'],
        params['module']
    )
    with open(params['output_file'], 'a') as f:
        f.write(write(parse_result))
        f.flush()


if __name__ == '__main__':
    main()

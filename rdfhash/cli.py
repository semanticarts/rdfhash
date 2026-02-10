import argparse
import sys
import logging

from rdfhash.main import hash_subjects, reverse_hash_subjects
from rdfhash.logger import logger
from rdfhash.utils import rdf_media_types, get_rdf_media_type
from rdfhash.utils.hash import hash_types
from rdfhash.utils.graph import graph_types


def get_parser() -> argparse.ArgumentParser:
    """Return argument parser for command 'hash_subjects'.
    
    Returns: 
        argparse.ArgumentParser: Argument parser for command 'hash_subjects'.
    """
    parser = argparse.ArgumentParser(
        description=(
            "Replace selected subjects with hash of their triples "
            "(`{predicate} {object}.\\n` sorted & joined)."
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument("data", nargs="+", help="Input RDF string or file path.")

    parser.add_argument(
        "-f",
        "--format",
        help="Input format.\nSupports: ['" + "', '".join(rdf_media_types) + "']",
        default="text/turtle",
    )

    parser.add_argument(
        "-g",
        "--graph",
        default="oxrdflib",
        help="Graph library to use.\nSupports: ['"
        + "', '".join(graph_types.keys())
        + "']",
    )

    parser.add_argument(
        "-a",
        "--accept",
        default="text/turtle",
        help="Output format.\nSupports: ['" + "', '".join(rdf_media_types) + "']",
    )

    parser.add_argument(
        "-t",
        "--template",
        default="{method}:{value}",
        help="Hash URI template. '{method}' corresponds to the hashing method (eg. 'sha256'). '{value}' corresponds to the calculated hash value.",
    )

    parser.add_argument(
        "-m",
        "--method",
        "--hash-method",
        default="sha256",
        help="Hash method.\nSupports: ['" + "', '".join(hash_types.keys()) + "']",
    )

    parser.add_argument(
        "-s",
        "--sparql",
        "--sparql-select-subjects",
        default="SELECT ?s WHERE { ?s ?p ?o . FILTER (isBlank(?s)) }",
        help="SPARQL SELECT query returning subject URIs to replace with hash of"
        " their triples. Defaults to all blank node subjects.",
    )

    parser.add_argument(
        "-r",
        "--reverse",
        action="store_true",
        help="Reverse hashed URIs to Blank Nodes. --template is used to identify hashed URI template.",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show 'info' level logs.",
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Show 'debug' level logs.",
    )

    return parser


def cli(args_list=None):
    """
    Parse arguments and pass to function 'hash_subjects'. Serialize results with
    respect to 'accept' argument.
    """
    # Parse arguments.
    if args_list == None:
        args_list = sys.argv[1:]
    parser = get_parser()
    args = parser.parse_args(["--help"] if len(args_list) == 0 else sys.argv[1:])

    # Convert --format to media type
    try:
        args.format = get_rdf_media_type(args.format)
    except ValueError as e:
        logger.error(
            f"Unsupported --format value.\n{e}"
        )
        sys.exit(1)

    # Convert --accept to media type
    try:
        args.accept = get_rdf_media_type(args.accept)
    except ValueError as e:
        logger.error(
            f"Unsupported --accept value.\n{e}"
        )
        sys.exit(1)

    if args.debug:
        logger.setLevel(logging.DEBUG)
    elif args.verbose:
        logger.setLevel(logging.INFO)

    graph, hashed_values = hash_subjects(
        args.data, args.format, args.method, args.template, args.sparql, args.graph
    )

    if args.reverse:
        reverse_hash_subjects(graph, args.format, args.template, args.graph)

    print(graph.serialize(format=args.accept))

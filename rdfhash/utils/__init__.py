import re
import mimetypes

from .hash import hash_types

mimetypes.add_type("text/turtle", ".ttl")
mimetypes.add_type("application/n-triples", ".nt")
mimetypes.add_type("application/trig", ".trig")
mimetypes.add_type("application/n-quads", ".nq")
mimetypes.add_type("application/rdf+xml", ".rdf")
mimetypes.add_type("text/n3", ".n3")

#: Supported RDF media types.
rdf_media_types = {
    "text/turtle",
    "application/n-triples",
    "application/trig",
    "application/n-quads",
    "application/rdf+xml",
    "text/n3",
}

#: Triple-based RDF media types.
triple_media_types = {
    "text/turtle",
    "application/n-triples",
}

#: RDF file type names to RDF media types.
rdf_alias_to_media_type = {
    "nquads": "application/n-quads",
    "ntriples": "application/n-triples",
    "turtle": "text/turtle",
    "xml": "application/rdf+xml",
    # Associate file extensions (without the leading dot) with RDF media types.
    **{mimetypes.guess_extension(mt)[1:]: mt for mt in rdf_media_types},
}


def get_rdf_media_type(format: str):
    """Convert a simplified RDF format string or media type to a supported RDF media type.

    Args:
        format (str): Simplified string or media type.

    Raises:
        ValueError: If 'format' is not related to a supported RDF media type.
    """
    format = format.lower()
    media_type = rdf_alias_to_media_type.get(format, format)
    if media_type not in rdf_media_types:
        raise ValueError(
            f"Invalid RDF format: {format}. Must be one of {rdf_media_types}."
        )
    return media_type


# TODO: Determine if this function is needed.
# I believe it's only used for converting hashed IRIs back to blank nodes.
def validate_uri(
    uri,
    template="{method}:{value}",
    values={"method": set(list(hash_types)), "value": r"[a-f0-9]+"},
):
    def value_re(value):
        if type(value) == set:
            return "(" + "|".join(value) + ")"
        elif type(value) == str:
            return value

    # Convert 'template' to a regular expression.
    template_re = template
    for key in values.keys():
        template_re = template_re.replace("{" + key + "}", value_re(values[key]))

    # Validate URI.
    return re.match(template_re, uri) != None

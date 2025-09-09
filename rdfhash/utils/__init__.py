import re

from .hash import hash_types

triple_mime_types = {
    "text/turtle",
    "application/n-triples",
}

rdf_ext_to_mime_types = {
    "ttl": "text/turtle",
    "nt": "application/n-triples",
    "trig": "application/trig",
    "nq": "application/n-quads",
    "rdf": "application/rdf+xml",
}
rdf_mime_types = {
    "text/turtle",
    "application/n-triples",
    "application/trig",
    "application/n-quads",
    "application/rdf+xml",
}


def get_rdf_mime_type(format: str):
    format = format.lower()
    mime_type = rdf_ext_to_mime_types.get(format, format)
    if mime_type not in rdf_mime_types:
        raise ValueError(
            "Invalid RDF format: {format}. Must be one of {rdf_mime_types}.".format(
                format=format, rdf_mime_types=rdf_mime_types
            )
        )


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

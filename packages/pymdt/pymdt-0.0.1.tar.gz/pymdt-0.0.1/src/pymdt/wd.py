from SPARQLWrapper import SPARQLWrapper, JSON
from importlib import metadata

# Property mapping for convenience and reference
property_mapping = {
    "DUNS_NUMBER": "https://www.wikidata.org/wiki/Property:P2771",
    "EIN": "https://www.wikidata.org/wiki/Property:P1297",
    "CIK": "https://www.wikidata.org/wiki/Property:P5531"
}


def build_user_agent():
    pkg_version = "/".join(
        [
            metadata.metadata('pymdt')['Name'],
            metadata.metadata('pymdt')['Version']
        ]
    )
    pkg_contact = "; ".join(
        [
            metadata.metadata('pymdt')['Home-page'],
            metadata.metadata('pymdt')['Author-email']
        ]
    )

    user_agent_string = f"Mozilla/5.0 ({pkg_contact}) {pkg_version}"
    return user_agent_string


def get_wd_by_property(
    property_name,
    endpoint_url="https://query.wikidata.org/sparql",
    user_agent=build_user_agent(),
    return_format="summarized"
):
    if property_name is None or property_name not in property_mapping:
        raise ValueError(f"You must supply a property_name as one of: {', '.join(list(property_mapping.keys()))}")

    query = """SELECT
      ?item ?itemLabel
      ?prop
    WHERE
    {
      ?item wdt:%s ?prop
      SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
    }
    """ % property_mapping[property_name].split(":")[-1]

    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    wikidata_results = sparql.query().convert()

    if return_format == "raw":
        return wikidata_results

    dataset = [
        {
            "wd_url": i["item"]["value"],
            "name": i["itemLabel"]["value"],
            property_name: i["prop"]["value"]
        } for i in wikidata_results["results"]["bindings"]
    ]

    return dataset

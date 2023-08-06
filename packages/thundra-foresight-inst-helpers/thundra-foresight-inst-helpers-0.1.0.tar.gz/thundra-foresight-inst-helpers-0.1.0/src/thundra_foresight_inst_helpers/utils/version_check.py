import urllib3
import xml.etree.ElementTree as et


def get_latest_version(repository: str, version: str = None) -> str:
    http = urllib3.PoolManager()
    response = http.request("GET", repository)
    xml = et.fromstring(response.data)

    available_versions = xml.findall("./versioning/versions/version")
    available_versions_set = set(map(lambda x: x.text, available_versions))

    latest_version = xml.find("./versioning/latest").text

    if version and (version in available_versions_set):
        return version
    else:
        return latest_version

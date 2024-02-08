import requests
import xml.etree.ElementTree as ET
from flask import Request
import re


class RequestOAI:
    def __init__(self, request: Request):
        self.request = request

    def request_oai(self, site_url, abbreviation):
        url = (
            f"{site_url}/oai?verb=ListRecords&metadataPrefix=oai_dc&set={abbreviation}"
        )
        response = requests.get(url)

        if response.status_code == 200:
            xml_data = response.content
            root = ET.fromstring(xml_data)

            records = root.findall(".//{*}record")
            resumption_token_element = root.find(".//{*}resumptionToken")

            parse_results = self.parse_oai(records)
            resumption_results = []

            if resumption_token_element is not None:
                resumption_token = resumption_token_element.text
                resumption_results = self.resumption_parse(resumption_token, site_url)

            combined_results = resumption_results + parse_results
            counts = len(combined_results)

            return {"results": combined_results, "counts": counts}

        else:
            error_message = {"error": "Failed to fetch data"}
            return error_message

    def resumption_parse(self, token, site_url):
        url = f"{site_url}/oai?verb=ListRecords&resumptionToken={token}"
        response = requests.get(url)

        if response.status_code == 200:
            xml_data = response.content
            root = ET.fromstring(xml_data)

            records = root.findall(".//{*}record")
            resumption_token_element = root.find(".//{*}resumptionToken")

            parse_results = self.parse_oai(records)
            resumption_results = []

            if resumption_token_element is not None:
                resumption_token = resumption_token_element.text
                resumption_results = self.resumption_parse(resumption_token, site_url)

            combined_results = resumption_results + parse_results
            return combined_results

        else:
            error_message = {"error": "Failed to fetch data"}
            return error_message

    def parse_oai(self, records):
        results = []

        for record in records:
            header = record.find("{*}header")
            metadata = record.find("{*}metadata")
            dc = metadata.find("{*}dc")

            articleId = header.find("{*}identifier").text.split("/")[-1]
            lastUpdate = header.find("{*}datestamp").text
            title = dc.find("{*}title").text
            creators = dc.findall("{*}creator")
            subjects = dc.findall("{*}subject")

            description_element = dc.find("{*}description")
            if description_element is not None:
                description = description_element.text
            else:
                description = " ";  

            publisher = dc.find("{*}publisher").text
            publishDate = dc.find("{*}date").text

            doi_elements = dc.findall("{*}identifier")
            if doi_elements:
                doi = doi_elements[-1].text
            else:
                doi = " " 

            sources = dc.findall("{*}source")[0].text
            fileView_elements = dc.findall("{*}relation")
            fileView = fileView_elements[0].text if fileView_elements else None


            sources_split = sources.split(";")

            journal = ""
            volume = ""
            issue = ""
            pages = ""

            if len(sources_split) > 0:
                journal_split = sources_split[0].strip().split(" ")
                journal = journal_split[1] if len(journal_split) > 1 else ""

            if len(sources_split) > 1:
                volume_issue_split = sources_split[1].strip().split(", ")
                if len(volume_issue_split) > 0:
                    volume = volume_issue_split[0].split(" ")[1] if volume_issue_split[0] else ""
                if len(volume_issue_split) > 1:
                    issue = volume_issue_split[1].split(" ")[1] if volume_issue_split[1] else ""
                    issue = ''.join(filter(str.isdigit, issue))

            if len(sources_split) > 2:
                pages = sources_split[2].strip()

            subjectsText = ([subject.text for subject in subjects],)

            subjectsText = subjects[0].text if subjects else ""

            if subjectsText:
                subjectsText = re.split(r", |; |,|;", subjectsText)
                subjectsText = [subject.title() for subject in subjectsText]
            else:
                subjectsText = []

            publishYear = publishDate.split("-")[0]

            creators_data = []

            for creator in creators:
                full_name = creator.text
                give_name, surname = full_name.split(", ")

                creator_object = {"name": f'{surname} {give_name}', "orcid": ""}
                creators_data.append(creator_object)

            results.append(
                {
                    "article_id": articleId,
                    "last_update": lastUpdate,
                    "title": title,
                    "creators": creators_data,
                    "subjects": subjectsText,
                    "description": description,
                    "publisher": publisher,
                    "publish_at": publishDate,
                    "publish_year": publishYear,
                    "doi": doi,
                    "isFeatured": False,
                    "file_view": fileView,
                    "journal": journal,
                    "volume": volume,
                    "issue": issue,
                    "pages": pages,
                }
            )

        return results
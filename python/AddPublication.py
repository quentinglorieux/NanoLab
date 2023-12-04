from pyalex import Works
import pyalex
import json
import sys
import re


pyalex.config.email = "quentin.glorieux@lkb.upmc.fr"


def extract_single_info(paper):

    match = re.search(r'physrev(.+?)(\d+)', paper["doi"])
    if match:
        if match.group(1)[0] not in ('l', 'r', 'x') : 
            if paper["primary_location"]["source"]["display_name"][-1] != match.group(1)[0].capitalize():
                journal_abbreviation = match.group(1)[0].capitalize()
            else : journal_abbreviation = ""
        else: journal_abbreviation = ""
    else: journal_abbreviation = ""

    return {
        'title': paper['title'],
        "authors": [
                {"name": entry["author"]["display_name"], "orcid": entry["author"]["orcid"]}
                for entry in paper["authorships"]
            ],
        'link': {
            'url' : paper['doi'],
            'display' :paper["primary_location"]["source"]["display_name"]
                + " "
                + str(paper["biblio"]["volume"])
                + " "
                + str(paper["biblio"]["issue"])
                + " ("
                + str(paper["publication_year"])
                + ").",
            },
        "doi": paper["doi"],
        "is_oa": paper["open_access"]["is_oa"],
        "oa_url": paper["open_access"]["oa_url"],
        "publication_year": paper["publication_year"],
        "journal": paper["primary_location"]["source"]["display_name"],
        "journal_abbreviation": journal_abbreviation,
        "biblio": paper["biblio"],
    }
    

# Export JSON file
def get_single_paper(doi):
    paper = Works()[doi]
    data = [extract_single_info(paper)]

    json_string = json.dumps(data, indent=2)

    # Save the JSON string to a file
    # with open("../_data/publications/last_add.json", "w") as file:
    #     file.write(json_string)

    with open("../_data/publications/full_list_openalex.json", 'r') as file:
        current_data = json.load(file)
        new_data = data + current_data
    with open("../_data/publications/full_list_openalex.json", 'w') as file:
        json.dump(new_data, file, indent=2)


def main():
    print(sys.argv)
    if len(sys.argv) != 2:
        print("Missing DOI arguement. Usage: python AddPublication.py <DOI> (ex : python AddPublication.py 'https://doi.org/10.7717/peerj.4375')")
        sys.exit(1)

    input_doi = sys.argv[1]
    print(f"DOI: {input_doi}")

    get_single_paper(input_doi)

if __name__ == "__main__":
    main()

import yaml


def main():
    ## Load and parse config file
    with open("config.yml", "r") as config_file:
        config_file = yaml.load(config_file, yaml.SafeLoader)

    # Populate Templates with Personal Data
    files_to_load = (
        "template/home.html",
        "template/menu.html",
    )
    home_template, menu_template = load_files(files_to_load)
    personal_details = config_file["Personal"]
    for tag, value in personal_details.items():
        home_template = home_template.replace(tag, value)

    primary_pubs = config_file["Primary Author Publications"]
    coauthor_pubs = config_file["Coauthor Publications"]

    menu_html = build_menu(primary_pubs, coauthor_pubs, menu_template)
    tag = "$MENU$"
    home_template = home_template.replace(tag, menu_html)

    # Building Home Page
    print("Building Homepage")
    build_home(coauthor_pubs, primary_pubs, home_template)
    print("Website Built!")


def build_menu(primary_pubs, coauthor_pubs, menu_template):
    pub_template = '<li><a href="$URL$">$TITLE$</a></li>'

    def process_pub_for_menu(pubs):
        entries = []
        for pub in pubs:
            entry = str(pub_template)
            for tag, value in pub.items():
                entry = entry.replace(tag, value)
            entries.append(entry)
        return "\n".join(entries)

    primary_pubs_html = process_pub_for_menu(primary_pubs)
    coauthor_pubs_html = process_pub_for_menu(coauthor_pubs)
    menu = menu_template.replace("$PRIMARY_PUBS$", primary_pubs_html).replace(
        "$COAUTHOR_PUBS$", coauthor_pubs_html
    )
    return menu


def build_home(primary_pubs, coauthor_pubs, home_template):

    publication_template = (
        '<article>\n<span class="icon fa-pencil"></span>'
        '<div class="content">'
        '<h3><a href="$URL$">$TITLE$</a></h3>'
        "<p>$BLURB$</p></div>\n</article>"
    )

    def process_pub_for_home_page(pubs):
        entries = []
        for pub in pubs:
            entry = str(publication_template)
            for tag, value in pub.items():
                entry = entry.replace(tag, value)
            entries.append(entry)
        return "\n".join(entries)

    primary_pubs_html = process_pub_for_home_page(primary_pubs)
    coauthor_pubs_html = process_pub_for_home_page(coauthor_pubs)

    payload = home_template.replace("$PRIMARY_PUBS$", primary_pubs_html).replace(
        "$COAUTHOR_PUBS$", coauthor_pubs_html
    )
    with open("index.html", "w") as page:
        page.write(payload)


def load_files(filenames):
    loaded_files = []
    for filename in filenames:
        with open(filename, "r") as file:
            loaded_files.append(file.read())
    return loaded_files


if __name__ == "__main__":
    main()

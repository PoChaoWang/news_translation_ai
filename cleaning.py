import os
import json
import re
import logging
import datetime
from bs4 import BeautifulSoup


def clean_data(data):
    """
    Data cleaning function to remove unwanted HTML tags and attributes from the content.
    Args:
        data (list): load from json file, list of dictionaries containing news data.
    Returns:
        list:  cleaned data, list of dictionaries with cleaned content.
    """
    for item in data:
        if "content" in item and isinstance(item["content"], str):

            soup = BeautifulSoup(item["content"], "html.parser")

            # record the status before cleaning
            has_alignright_before = bool(soup.select("div.alignright"))
            logging.debug(
                f"Before cleaning: has alignright div: {has_alignright_before}"
            )

            # remove all specific tags
            tags_to_remove = [
                "span",
                "strong",
                "em",
                "section",
                "small",
                "figcaption",
                "img",
                "figure",
                "script",
                "h4",
            ]
            for tag_name in tags_to_remove:
                for tag in soup.find_all(tag_name):
                    tag.decompose()

            # remove specific classes
            class_selectors = {
                "ul": ["lcp_catlist"],
                "div": ["tnp", "tnp-subscription", "alignright"],
                "p": ["text-above-ad"],
            }

            for tag_name, class_list in class_selectors.items():
                for class_name in class_list:
                    for tag in soup.find_all(
                        tag_name, class_=lambda x: x and class_name in x
                    ):
                        tag.decompose()

            # remove specific IDs
            id_selectors = ["article-mpu"]
            for id_prefix in id_selectors:
                for tag in soup.find_all(id=lambda x: x and x.startswith(id_prefix)):
                    tag.decompose()

            # remove specific IDs with "snack_dex"
            for tag in soup.find_all(id=lambda x: x and "snack_dex" in x):
                tag.decompose()

            # record the status after cleaning
            has_alignright_after = bool(soup.select("div.alignright"))
            logging.debug(f"After cleaning: has alignright div: {has_alignright_after}")

            # replace <a> tags with <b> tags
            a_tags = soup.find_all("a")
            for a_tag in a_tags:
                b_tag = soup.new_tag("b")
                b_tag.string = a_tag.get_text()
                a_tag.replace_with(b_tag)

            unwanted_texts = [
                "Become a RaceFans supporter",
                "Go ad-free for just £1 per month",
                "Find out more and sign up",
            ]
            for text in unwanted_texts:
                # remove unwanted text
                for text_node in soup.find_all(text=True):
                    if text in text_node:
                        # if the text is in a tag, remove the tag
                        text_node.replace_with(text_node.replace(text, ""))

            item["content"] = str(soup)
            item["translation_status"] = "pending"
            item["content_zh"] = ""

    # filter out items without content
    cleaned_data = [item for item in data if item.get("content")]
    return cleaned_data


def merge_and_clean_data(news_data, output_dir=None, debug=False):
    """
    Merge and clean news data from different sources.
    Args:
        news_data (list): list of dictionaries containing news data.
        output_dir (str, optional): path to save the cleaned data file (used only when debug=True).
    Returns:
        list: cleaned data, list of dictionaries with cleaned content.
    """
    seen_links = set()
    unique_data = []

    # remove duplicates by link
    for item in news_data:
        link = item.get("link")
        if link and link not in seen_links:
            seen_links.add(link)
            unique_data.append(item)

    cleaned_data = clean_data(unique_data)
    executed_at = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")

    if debug and output_dir:
        os.makedirs(output_dir, exist_ok=True)
        fetch_path = os.path.join(output_dir, f"all_cleaned_data_{executed_at}.json")
        with open(fetch_path, "w", encoding="utf-8") as f:
            json.dump(cleaned_data, f, ensure_ascii=False, indent=4)
        logging.info(f"Cleaned data saved to {output_dir}")
    else:
        logging.info("Debug mode is off in Step 2, not saving translated data.")

    return cleaned_data

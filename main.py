from typing import Optional
import re
import pandas as pd
from collections import defaultdict
import click


def select_set_of_authors(df: pd.DataFrame) -> set:
    """
    Extract all authors from `authors` column.
    Each row of authors column is string representation of list of authors.

    :param df: A DataFrame containing authors column.
    :return: Set of authors
    :rtype: set.
    """

    authors_df = df[~df.authors.isna()]

    authors = set()
    for row in authors_df.authors:
        authors |= set(eval(row))
    return authors


def select_candidate_name(author: str) -> Optional[str]:
    """
    Assuming author can have one or more names, select one which is not prefix or not one-letter.
    :param author: String with author names.
    :return: One name
    :rtype: Optional[str, None]
    """

    def filters(x):
        if x in ["st", "van", "der", "de", "ll", "md", "le", "da", "la", "den", "el"]:
            # Reject common prefixes
            return False
        if len(x) > 1 and x.isalpha():
            # Accept two or more letters word if all characters are letters
            return True
        if len(x) > 4:
            # Accept words with any character longer than 4
            return True
        return False

    choice = None
    for candidate in author.split(" "):
        if filters(candidate):
            choice = candidate
            break
    return choice


def split_author(author: str) -> (str, str):
    """
    Split author by white character and lower the result.
    Return author's names and lastname.
    :param author: Full author name
    :return: list of names and lastname
    :rtype: tuple
    """
    author_list = re.sub(" +", " ", author).lower().split(" ")
    return " ".join(author_list[:-1]), author_list[-1]


def unique_authors(authors: set) -> pd.DataFrame:
    """
    Remove authors with undefined names - one letter, abbreviation etc..
    Prepare list of unique authors
    :param authors: Set of authors.
    :return: Set of unique authors.
    :rtype: set
    """
    by_surname = defaultdict(set)
    for author in authors:
        # split = re.sub(" +", " ", author).lower().split(" ")
        # lastname = split[-1]
        names, lastname = split_author(author=author)
        name = select_candidate_name(names)
        if name is not None:
            by_surname[lastname].add(name)

    result = []
    for lastname, candidates in by_surname.items():
        for name in candidates:
            result.append((name.capitalize(), lastname.capitalize()))
    return pd.DataFrame(result, columns=["firstname", "lastname"])


@click.command()
@click.option(
    "--path", help="Path to csv file", required=True, type=click.Path(exists=True)
)
def main(path):
    """
    This program read data from provided csv file with column `authors`
    and returns set of unique authors.
    """
    print("reading data ..")
    df = pd.read_csv(path)
    print("done")
    print("preparing results...")
    authors = select_set_of_authors(df=df)

    unique_authors_df = unique_authors(authors=authors)
    unique_authors_df = unique_authors_df.sort_values(by=["lastname", "firstname"])
    unique_authors_df.to_csv("unique_people.csv", index=False)
    print("done")


if __name__ == "__main__":
    main()

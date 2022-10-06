"""potatoes"""


def get_markdown_from_docs(docs: str) -> str:
    """
    get markdown from the __doc__
    after the :math: marker
    """
    # AttributeError: 'NoneType'
    try:
        markdown = docs.split(":math:")[1]
        # remove quotes `
        markdown = docs.split("`")[1]
        markdown = markdown.replace("`", "")

        # add the $$ to the markdown
        markdown = "$$" + markdown + "$$"
    except AttributeError:
        markdown = "formula malformed, check the docstring"
    except IndexError:
        markdown = "no formula marker :math: in docstring"

    return markdown

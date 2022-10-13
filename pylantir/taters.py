#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" *Po-tay-toes!* Boil 'em, mash 'em, stick 'em in a stew... 
Lovely big golden chips with a nice piece of fried fish."""


def get_markdown_from_docs(docs: str) -> str:
    """
    get markdown from the __doc__ so it can be printed with IPython.display.Markdown in notebook
    after the :math: marker, in between "`" quotes (for sphinx)
    """
    # AttributeError: 'NoneType'
    try:
        markdown = docs.split(":math:")[1]
        
        markdown = docs.split("`")[1]
        markdown = markdown.replace("`", "")
        # add "$$" to make it a mathjax equation with .join
        markdown = markdown.join(["$$", "$$"])
        
    except AttributeError:
        markdown = "formula malformed, check the docstring"
    except IndexError:
        markdown = "no formula marker :math: in docstring"

    return markdown
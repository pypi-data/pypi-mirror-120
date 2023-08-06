# WEBPAGE ANALYSIS TOOL

This tool extracts insight from a webpage. The insights that can be extracted are:
- all unique tags used in the document.
- the most commonly used tag.
- the longest path starting from root node to the descendent.
- the longest path starting from root node where the most popular tag is used the most times.

# Installation 

``` python
    $ pip install webanalytictool
```

``` python
    from analytic import WebPageAnalyticTool
```

# Usage
To create an object of WebPageAnalyticTool,
```
    $ url = 'https://www.bbc.com/sport/football'
    $ wat = WebPageAnalyticTool(url)
```

To get `longest path starting from root node to the descendent`
``` python
    $ wat.get_longest_path
```

To get `the longest path starting from root node where the most popular tag is used the most times`

``` python
    $ wat.get_longest_path_with_most_common_tag
```

To get `the most commonly used tag`

``` python
    $ wat.get_most_common_tags
```

To get `all unique tags used in the document`

``` python
    $ wat.get_unique_tags
```
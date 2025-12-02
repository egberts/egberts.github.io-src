title: Viewing extremely large DOT or GV graph
date: 2022-09-15 07:15
modified: 2025-07-13 01:56
status: published
tags: DOT, tulip, graphviz, python3-graphviz, SVG, Python, python-graphviz, bison
category: HOWTO
summary: How to view an extremely large DOT or GV graph effectively

Creating layout a 
[DOT graph](https://en.wikipedia.org/wiki/DOT_\(graph_description_language\))
is that final step before visualizing the raw data.

And as the DOT file gets bigger and bigger, the many existing image viewers 
start to crash or hang.

This article details the many ways on how to visualize extra-large 
DOT graph files, especially if you have a small computer.

In this article, we use:

* [Bison](https://www.gnu.org/software/bison/)
* [pygraphviz](https://pygraphviz.github.io/)
* [Graphviz](https://en.wikipedia.org/wiki/Graphviz)
* [eog, Eye of GNOME](https://gitlab.gnome.org/GNOME/eog)

To install on Debian, the Debian package names are:
```bash
apt install  bison eog graphviz python3-pygraphviz pygraphviz
```

# DOT graph

DOT graph is a text-based file containing information on nodes and edges
as well as the entire graph.

Many
[tools](https://en.wikipedia.org/wiki/DOT_(graph_description_language)#Layout_programs) 
can create a layout from a DOT graph so that various tools can
create an image from.


# Python

To work with the file format of DOT graph, I've evaluated several Python APIs:
* [graph-tool](https://en.wikipedia.org/wiki/Graph-tool), uses Boost Graph
  library
* [python3-graphviz](https://github.com/xflr6/graphviz)
* [pygraphviz](https://pygraphviz.github.io/)
* [NetworkX](https://networkx.github.io/)

I needed the ability to 
selectively view only a portion of this DOT large graph,
since I've been working with 
[NFTABLES nft CLI](https://wiki.nftables.org/),
the largest degree-spanning DOT graph tree, to date.

Clustering and statistical anomalies do not matter here.


# nftable parser graph

We obtain the DOT graph from `nftables` by executing `bison`:

```console
$ cd /tmp
$ git clone https://git.netfilter.org/nftables
$ cd nftables/src
$ bison --graph parser_bison.y
$ # DOT graph file, parser_bison.dot, gets created here
```


# Converting DOT to SVG

With the created DOT graphviz file (`parser_bison.dot`), we can now create graphs from it.

## pygraphviz API
And to work with large DOT graph, specifically of a LR-parser nature, 
I have chosen `pygraphviz` to be this glue, a Python API glue.


# Node-selecting Python script
The opening of large but viewable GV (or DOT) file is done by doing:
```python
#!/usr/bin/env python3

import subprocess
import pygraphviz

# input_file='/tmp/parser.gv'  # current filetype, not used here
input_file='./parser_bison.dot'  # alternative older filetype

image_file='./parser_bison.svg'

print('Reading %s as DOT graph.' % input_file)
graph = pygraphviz.AGraph(
                   name='myGraph', 
                   filename=input_file, 
                   directed=True, 
                   strict=False
                  )
graph.layout(prog='dot')  # read DOT-format
graph.draw(image_file)
print('File %s created.' % image_file)

bash_command = "eog " + a_image_file
process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
print('Spawning eog as a SVG viewer.')
process.communicate()
```

It's that simple using an `eog` SVG viewer.  However, DOT graph with more than 10 degrees of depth are not so easily handled by other image viewers.  And LR-parser often has 30-200 degrees, notably `nftables` having 124 degrees.

## IT'S TOO BIG
At least you can view the graph but all that zooming in (using a mouse wheel)
and moving the zoomed view pane (using mouse-button hold down) can be
a bit tiring.  

I'm a bit tiring after working with N-degree graph tree:
zoom, zoom, zoom, view-drag, view-drag, view-drag, zoom, zoom, zoom.

Some alternatives to try for extremely large DOT graph files are:


* [Gephi](https://github.com/gephi/gephi)

PRUNE THE TREE
==============
The graph tree can be selectively pruned to get what one desires.  And I want 
that.

```python
# Filter to just Node 12, 50, and 59
new_graph = filter_nodes(graph, [u'12', u'50', u'59'])
```

This filter node will copy all nodes and edges associated with node
12, 50, and 59.  Bonus is all attributes are copied as well into 
this `new_graph`.

And the new filter routine is:
```python
def filter_nodes(g, target_node):
    node_list = []
    node_list.extend(target_node)
    new_g = pgv.AGraph(name='newDigraph', directed=True, strict=False)
    copy_graph_attr(g, new_g)
    for v, u in g.edges():
        if str(v) in target_node:
            node_list.extend({u})
            print("Added ", u)
            if True:  # g.has_edge(v, u):
                old_edge = g.get_edge(v, u)
                new_g.add_edge(v, u)
                new_edge = new_g.get_edge(v, u)
                for fn_key in old_edge.attr.keys():
                    print('%s, %s, %s:' % (v, u, fn_key))
                    print('%s, %s, %s=%s' % (v, u, fn_key, old_edge.attr[fn_key]))
                    value = old_edge.attr[fn_key]
                    new_edge.attr[fn_key] = value

    # reduce list using set()
    node_list = list(set(node_list))
    for n in node_list:
        if g.has_node(n):
            new_g.add_node(n, name=None)
            old_node = g.get_node(n)
            new_node = new_g.get_node(n)
            for b_key in old_node.attr.keys():
                new_node.attr[b_key] = old_node.attr[b_key]
    return new_g
```

This makes me happy.

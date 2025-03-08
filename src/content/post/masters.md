---
layout: ../../layouts/post.astro
title: "Masters Thesis: Geocoding via LINZ Address Matching"
description: A free offline geocoding tool for NZ Addresses
dateFormatted: Feb 28th, 2025
---

This post is about my personal project turned masters - GLAM. You can view the thesis [here](https://r2.lmor152.com/GLAM%20Thesis.pdf).

Geocoding via LINZ Address Matching (GLAM) is a Python package I began building during the covid lockdowns since I couldn't leave the house. I had noticed that geocoding is a very common and expensive problem for our clients during my work as a Data Science Consultant at KPMG. I thought it couldn't be that hard, so I decided to take a crack at it.

As it turns out, address matching is ***hard***. Addresses come in all sorts of formats, with colloquialisms, abbrevations, typos, and often with random extra information. The Auckland Art Gallery is located on `Wellesley Street East, Auckland Central, Auckland 1010`, but it could also be addressed as any of the following:
* Auckland Art Gallery
* Wellesley St E, Auckland
* Level 2, AAG, Wellesley St E AKL

Considering all possible abbreviations of cities, street types, cardinal directions is a difficult task. On top of that, algorithms need to be ***fast***. NZ has over 2 million addresses, so even if you can make a million address comparisons per second, you are only geocoding 1 address every 2 seconds. This quickly becomes intractable for datasets with tens or hundreds of thousands of addresses that need geocoding. This means that intelligent search methods are often required on top of clever address comparison methods.

After completing the first version of the package, I presented it to some professors at The University of Auckland, and found that with a little more academic rigour, it could be turned into a research project for a master's degree in Operations Research and Analytics. Two years later, the package has been upgraded to support multiple methods of geocoding NZ addresses, and it's freely available to everyone via:
* [GitHub](https://github.com/lmor152/glam)
* [Demo Site](https://glam-demo.lmor152.com)
* [PyPI / PIP](https://pypi.org/project/glam/)

## How it works

Algorithms are divided into ***address parsers***, and ***address matchers***. 

### Parsing
Address parsers convert an unstructured address into its composite parts like so:

<table>
  <tr>
    <td style="vertical-align: middle;">Third floor 70 Symonds St, Grafton 1010</td>
    <td style="vertical-align: middle;">➜</td>
    <td style="vertical-align: middle;">
      <pre>
{
    "level": 3
    "first_number": "70",
    "street_name": "Symonds Street", 
    "suburb_town_city": "Grafton",
    "postcode": "1010"
}</pre>
    </td>
  </tr>
</table>

The parser I built for GLAM uses an RNN to classify each character, and sigmoid activation means each character is given a probability of belonging to each class label. For an example input address `3rd floor 18 viaduct harbour rd`, you can visualise these probabilities in a heatmap:

![pic](/assets/images/projects/masters/rnn_heatmap.svg)

I also implemented a wrapper around the [libpostal parser](https://github.com/openvenues/libpostal).

### Matching
Address matching algorithms take either an unparsed or parsed address and find the best matching address in the New Zealand Street Address database, including coordinates. I implemented a few methods for matching:
* Fuzzy
* TF-IDF
* Compositional Vectors (my proposed method)
* Address Embeddings
* Some hybrid approaches

There's too much detail to cover for each of these, but a brief description of each is:
* Fuzzy: Fuzzy matches each part of a parsed address to the lookup database (with smart reductions to the search space) and returns the best match based on a weighted similarity score.
* TF-IDF: Uses character bigram counts with weighted importances to vectorise addresses, then cosine similarity to find the nearest neighbour in the vector space.
* Address Embeddings: Uses a transformer-encoder model to create address embeddings, then a KD-tree to quickly find the best matching embedding in the lookup database.
* Compositional Vectors: Intelligently composes vectors based on the shape and distribution of characters in addresses, and uses a KD-tree to find the closest match in the lookup database.

## Results

The final results from my thesis compared these methods to leading geocoding APIs. GLAM is able to provide accuracy and robustness that rivals the best commercial geocoders, the single threaded speed is faster than calling APIs directly too.

| Matcher/API | Accuracy | Robustness | Max Rate (addresses/sec) | Actual Rate (addresses/sec) |
|-------------|----------|------------|------------|---------------|
| Google      | A+       | A+         | 50         | 3.93          |
| AWS         | A+       | A          | 100        | 11.6          |
| Azure       | A+       | B-         | 50         | 1.10          |
| Mapbox      | A+       | A-         | 1000       | 1.85          |
| Nominatim   | A        | F          | 1          | 1.00          |
||||||
| TF-IDF      | A+       | A+         | -          | 20.5          |
| Fuzzy       | A+       | A          | -          | 10.2          |
| CV          | A        | C          | -          | 436           |
| Embedding   | B-       | F          | -          | 51.6          |

### Grading scale

| Grade | Percentage Range |
|-------|------------------|
| A+    | 95--100%         |
| A     | 90--94%          |
| A-    | 85--89%          |
| B+    | 80--84%          |
| B     | 75--79%          |
| B-    | 70--74%          |
| C+    | 65--69%          |
| C     | 60--64%          |
| C-    | 55--59%          |
| F     | Below 59%        |


Next time you need to do some goecoding on NZ addresses, give GLAM a try! There is a user guide with the [repo](https://github.com/lmor152/glam). Let me know how you get on 😊



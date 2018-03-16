# TinderMatch
TinderMatch is based on Natural Language Processin and  Computer Vision to rank Tinder profiles and automatically swipes right on all those which pass the promiscuity test.

*Read more in blog post here: [FarhanAnsari/TinderMatch](http://farhanansari.in/2018/03/16/sounds-tinder-with-ml/).*

# Tech
* The unofficial <a href="https://gist.github.com/rtt/10403467">Tinder API documentation</a> and <a href="https://github.com/charliewolf/pynder">Pynder</a> (A Python client for the API) to interact with Tinder.
* Django framework to deploy the webapp.
* A modified version of <a href="https://github.com/ParthGandhi/nude.py">nude.py</a> to analyse images for nudity/semi-nudity and assign scores based on skin pixel percentage. (Which is funny, because this algorithm is actually used in pornography blocking software.) 
* A <a href="https://github.com/aneesha/RAKE">Python implementation of the Rapid Automatic Keyword Extraction (RAKE) algorithm</a> to perform simple sentiment analysis. Keywords extracted from the bio using the algorithm are matched with a custom dictionary of keywords to obtain a score for the text.
* <a href="https://howhot.io/">Howhot.io</a> to rate images on a general level of attractiveness. (To-do)

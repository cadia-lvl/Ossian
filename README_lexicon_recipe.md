



# Ossian + DNN demo with lexicon

For setup and naive recipe without a lexicon, please see ```README.md``` (note that Ossian is implemented in Python 2.7)


# DNN-based voice using a recipe with lexicon

Ossian trains voices according to a given 'recipe' -- the recipe specifies a sequence of processes which are applied to an utterance to turn it from text into speech, and is given in a file called ```$OSSIAN/recipes/<RECIPE>.cfg``` (where ```<RECIPE>``` is the name of a the specific recipe you are using). A recipe called ```naive_01_nn``` is described in ```README.md```. Here we will describe the ```lex_01_nn``` recipe. If you want to add components to the synthesiser, the best way to start will be to take the file for an existing recipe, copy it to a file with a new name and modify it.
	
### Language resources

For TTS training with a lexicon you need at least a pronunciation dictionary (lexicon), and a phoneset definition. More advanced NLP can involve e.g. part-of-speech tagging, see the [English gold standard recipe](http://homepages.inf.ed.ac.uk/owatts/ossian/html/gold_standard_recipes.html) 


### Sequitur g2p
Ossian takes care of training a g2p model based on your lexicon, using the [Sequitur g2p toolkit](https://www-i6.informatik.rwth-aachen.de/web/Software/g2p.html). Be sure to add the ```$OSSIAN/tools/patch/sequitur_compilation.patch``` to the ```setup.py``` of Sequitur before installing, at least if you are using MacOS. If you place Sequitur in ```$OSSIAN/tools``` and run the following from the ```g2p``` directory: ```python setup.py install --prefix $OSSIAN/tools``` , everything will be set up as Ossian expects.

If you use another setup, you have to change the g2p paths in ```$OSSIAN/scripts/processors/Lexicon.py```

### lex_01\_nn.cfg

This is the configuration for a basic lexicon based training. You might have to adjust this file, some examples:

Change the dictionary parameter for the Lexicon class:
```
phonetiser = Lexicon('segment_adder', target_nodes="//token", target_attribute='text', child_node_type='segment', \
                            class_attribute='token_class', output_attribute='pronunciation', word_classes = ['word'], \
                            probable_pause_classes = ['punctuation', c.TERMINAL], possible_pause_classes=['space'],\
                            dictionary='my_dictionary_directory', lts_ntrain=1000, lts_gram_length=2)

``` 

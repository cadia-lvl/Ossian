



# Ossian + DNN demo with lexicon

For setup and naive recipe without a lexicon, please see ```README.md``` (note that Ossian is implemented in Python 2.7)


# DNN-based voice using a lex recipe

Ossian trains voices according to a given 'recipe' -- the recipe specifies a sequence of processes which are applied to an utterance to turn it from text into speech, and is given in a file called ```$OSSIAN/recipes/<RECIPE>.cfg``` (where ```<RECIPE>``` is the name of a the specific recipe you are using). A recipe called ```naive_01_nn``` is described in ```README.md```. Here we will describe the ```lex_01_nn``` recipe. If you want to add components to the synthesiser, the best way to start will be to take the file for an existing recipe, copy it to a file with a new name and modify it.
	
### Language resources

For TTS training with a lexicon you need at least a pronunciation dictionary (lexicon), and a phoneset definition. More advanced NLP can involve e.g. part-of-speech tagging, see the [English gold standard recipe]http://homepages.inf.ed.ac.uk/owatts/ossian/html/gold_standard_recipes.html 


### Sequitur g2p
Ossian takes care of training a g2p model based on your lexicon, using the [Sequitur g2p tool]https://www-i6.informatik.rwth-aachen.de/web/Software/g2p.html. Be sure to add the ```$OSSIAN/tools/patch/sequitur_compilation.patch``` to the ```setup.py``` of Sequitur before installing. If you place Sequitur in ```$OSSIAN/tools``` and run the following from the ```g2p``` directory, everything will be set up as Ossian expects: ```python setup.py install --prefix $OSSIAN/tools``` 

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


```
cd $OSSIAN
export THEANO_FLAGS=""; python ./tools/merlin/src/run_merlin.py $OSSIAN/train/rm/speakers/rss_toy_demo/naive_01_nn/processors/duration_predictor/config.cfg
```

For this toy data, training on CPU like this will be quick. Alternatively, to use GPU for training, do:

```
./scripts/util/submit.sh ./tools/merlin/src/run_merlin.py $OSSIAN/train/rm/speakers/rss_toy_demo/naive_01_nn/processors/duration_predictor/config.cfg
```

If training went OK, then you can export the trained model to a better format for Ossian. The basic problem is that the NN-TTS tools store the model as a Python pickle file -- if this is made on a GPU machine, it can only be used on a GPU machine. This script converts to a more flexible format understood by Ossian -- call it with the same config file you used for training and the name of a directory when the new format should be put:

```
python ./scripts/util/store_merlin_model.py $OSSIAN/train/rm/speakers/rss_toy_demo/naive_01_nn/processors/duration_predictor/config.cfg $OSSIAN/voices/rm/rss_toy_demo/naive_01_nn/processors/duration_predictor
```

When training the duration model, there will be loads of warnings saying ```WARNING: no silence found!``` --  theses are not a problem and can be ignored.

Similarly for the acoustic model:

```
cd $OSSIAN
export THEANO_FLAGS=""; python ./tools/merlin/src/run_merlin.py $OSSIAN/train/rm/speakers/rss_toy_demo/naive_01_nn/processors/acoustic_predictor/config.cfg
```

Or:

```
./scripts/util/submit.sh ./tools/merlin/src/run_merlin.py $OSSIAN/train/rm/speakers/rss_toy_demo/naive_01_nn/processors/acoustic_predictor/config.cfg
```

Then:

```
python ./scripts/util/store_merlin_model.py $OSSIAN/train/rm/speakers/rss_toy_demo/naive_01_nn/processors/acoustic_predictor/config.cfg $OSSIAN/voices/rm/rss_toy_demo/naive_01_nn/processors/acoustic_predictor
```



If training went OK, you can synthesise speech. There is an example Romanian sentence in ```$OSSIAN/test/txt/romanian.txt``` -- we will synthesise a wave file for it in ```$OSSIAN/test/wav/romanian_toy_naive.wav``` like this:

```
mkdir $OSSIAN/test/wav/

python ./scripts/speak.py -l rm -s rss_toy_demo -o ./test/wav/romanian_toy_HTS.wav naive_01_nn ./test/txt/romanian.txt
```

You can find the audio for this sentence [here](https://www.dropbox.com/s/xm9d7j7125y6j13/romanian_test_sentence_reference.wav?dl=0) for comparison (it was not used in training).

The configuration files used for duration and acoustic model training will work as-is for the toy data set, but when you move to other data sets, you will want to experiment with editing them to get better permformance.
In particular, you will want to increase training_epochs to train voices on larger amounts of data; this could be set to e.g. 30 for the acoustic model and e.g. 100 for the duration model.
You will also want to experiment with learning_rate, batch_size, and network architecture (hidden_layer_size, hidden_layer_type). Currently, Ossian only supports feed-forward networks.





# Other recipes

We have used many other recipes with Ossian which will be documented here when cleaned up enough to be useful to others. These will give the ability to add more  knowledge to the voices built, in the form of lexicons, letter-to-sound rules etc., and integrate existing trained components where they are available for the target language. 










add instructions on adding more text